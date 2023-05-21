from odoo import fields, api, models


class Order(models.Model):
    _name = 'cy.order'
    _description = '''订单信息'''
    _sql_constraints = [('order_no_unique', 'UNIQUE(order_no)', '订单号不可重复')]
    _order = "id desc"

    order_no = fields.Char(string='订单号', required=True, size=63)
    user_id = fields.Many2one('cy.user', string='用户', index=True)

    shipping_method = fields.Char(string='物流方式', required=True, size=31)
    shipping_method_id = fields.Char(string='物流方式ID', required=True, size=31)
    shipping_link = fields.Char(string="物流信息说明连接", size=255)
    shipping_subtitle = fields.Char(string="物流信息默认子标题", size=255)

    shipping_fee = fields.Integer(string='快递费', required=True)
    market_subtotal_fee = fields.Integer(string='市场价格', required=True)
    subtotal_fee = fields.Integer(string='小计', required=True)
    insured_fee = fields.Integer(string='保险费')
    promotion_deduct = fields.Integer(string='活动折扣')
    payment_deduct = fields.Integer(string='实际支付金额')

    promotion_rules = fields.One2many('cy.order.promotion.rule', 'order_id', string='折扣相关')

    currency = fields.Char(string='币种', size=7)
    from_usd_rate = fields.Float(string='汇率', default=1)

    payment_channel = fields.Selection(selection=[('paypal', 'paypal')], string='支付方式', default='1', size=31)

    real_pay = fields.Float(string='实际支付')
    pay_date = fields.Datetime(string='支付时间')
    shipping_date = fields.Datetime(string='发货时间')
    received_date = fields.Datetime(string='确认收获时间')

    status = fields.Selection(selection=[('1', '等待支付'), ('2', '等待发货'), ('3', '等待收货'), ("5", '已取消'), ("6", '已完成')], string='订单状态', size=31)
    is_commented = fields.Boolean(string="是否已评价", default=False)

    address = fields.One2many('cy.order.address', 'order_id', string='配送地址', required=True)
    items = fields.One2many('cy.order.item', 'order_id', string='订单条目')

    shippings = fields.One2many('cy.order.shipping', 'order_id', string='物流信息')
    shipping_json = fields.Text(string='物流信息')

    cancel_reason = fields.Char(string='取消原因', size=500)

    usd_shipping_fee = fields.Float(string='快递费(USD)', compute="_usd_fee")
    usd_subtotal_fee = fields.Float(string='小计(USD)', compute="_usd_fee")
    usd_market_subtotal_fee = fields.Float(string='市场价格(USD)', compute="_usd_fee")
    usd_insured_fee = fields.Float(string='保险费(USD)', compute="_usd_fee")
    usd_promotion_deduct = fields.Float(string='活动折扣(USD)', compute="_usd_fee")
    usd_payment_deduct = fields.Float(string='实际支付(USD)', compute="_usd_fee")

    currency_shipping_fee = fields.Float(string='快递费', compute="_currency_fee")
    currency_subtotal_fee = fields.Float(string='小计', compute="_currency_fee")
    currency_market_subtotal_fee = fields.Float(string='市场价格', compute="_currency_fee")
    currency_insured_fee = fields.Float(string='保险费', compute="_currency_fee")
    currency_promotion_deduct = fields.Float(string='活动折扣', compute="_currency_fee")
    currency_payment_deduct = fields.Float(string='实际支付', compute="_currency_fee")

    is_delete = fields.Boolean(string='已删除', default=False)
    track_info = fields.Text(string='埋点信息')
    active = fields.Boolean(string='是否有效', default=True, index=True)

    from_platform = fields.Char(string="支付平台", size=31, compute='_compute_from_platform', store=False)

    @api.depends('order_no')
    def _compute_from_platform(self):
        for record in self:
            payorders = self.sudo().env['cy.payment.payorder'].search([('biz_order_no', '=', record.order_no)])
            if len(payorders) > 0:
                record.from_platform = payorders[0].from_platform
            else:
                record.from_platform = ''

    def _usd_fee(self):
        conv = self.env['cy.base']
        for record in self:
            record.usd_insured_fee = conv.money_to_usd(record.insured_fee, record.currency, record.from_usd_rate)
            record.usd_shipping_fee = conv.money_to_usd(record.shipping_fee, record.currency, record.from_usd_rate)
            record.usd_market_subtotal_fee = conv.money_to_usd(record.market_subtotal_fee, record.currency, record.from_usd_rate)
            record.usd_subtotal_fee = conv.money_to_usd(record.subtotal_fee, record.currency, record.from_usd_rate)
            record.usd_promotion_deduct = conv.money_to_usd(record.promotion_deduct, record.currency, record.from_usd_rate)
            record.usd_payment_deduct = conv.money_to_usd(record.payment_deduct, record.currency, record.from_usd_rate)

    def _currency_fee(self):
        conv = self.env['cy.base']
        for record in self:
            record.currency_insured_fee = conv.money_int_to_float(record.insured_fee, record.currency)
            record.currency_shipping_fee = conv.money_int_to_float(record.shipping_fee, record.currency)
            record.currency_market_subtotal_fee = conv.money_int_to_float(record.market_subtotal_fee, record.currency)
            record.currency_subtotal_fee = conv.money_int_to_float(record.subtotal_fee, record.currency)
            record.currency_promotion_deduct = conv.money_int_to_float(record.promotion_deduct, record.currency)
            record.currency_payment_deduct = conv.money_int_to_float(record.payment_deduct, record.currency)


class PromotionRule(models.Model):
    _name = 'cy.order.promotion.rule'
    _description = '订单参与的折扣信息'

    order_id = fields.Many2one('cy.order', string='订单ID')
    rule_id = fields.Integer(string='规则ID')
    name = fields.Char(string='活动名称', size=63)
    deduct = fields.Integer(string='扣减')
    usd_deduct = fields.Float(string='美元扣减', compute="_usd_fee")
    currency_deduct = fields.Float(string='扣减', compute="_usd_fee")
    coupon_code_id = fields.Integer(string='优惠券ID')

    def _usd_fee(self):
        conv = self.env['cy.base']
        for record in self:
            record.usd_deduct = conv.money_to_usd(record.deduct, record.order_id.currency, record.order_id.from_usd_rate)
            record.currency_deduct = conv.money_int_to_float(record.deduct, record.order_id.currency)


class OrderAddress(models.Model):
    _name = 'cy.order.address'
    _description = '''配送地址'''
    _sql_constraints = [('order_id_unique', 'UNIQUE(order_id,address_type)', '一个订单一个收货地址')]

    order_id = fields.Many2one('cy.order', string='订单ID', index=True)

    first_name = fields.Char('First Name', size=31)
    last_name = fields.Char('Last Name', size=31)
    phone_number = fields.Char('Phone Number', size=64)
    address_line1 = fields.Char('Address Line 1', size=127)
    address_line2 = fields.Char('Address Line 2', size=127)
    post_code = fields.Char(string="Post/Zip Code", size=31)
    tax_number = fields.Char(string="Tax Number", size=63)
    country = fields.Char(string="Country/Region", size=63)
    state = fields.Char(string="State/Province", size=63)
    city = fields.Char(string="City", size=63)
    country_region_id = fields.Integer(string="Country/Region ID")
    state_region_id = fields.Integer(string="State/Province ID")
    city_region_id = fields.Integer(string="City ID")

    address_type = fields.Selection(selection=[('1', '收货地址'), ('2', '账单地址')], default="1", size=31)


class OrderItem(models.Model):
    ''' cy_order_item '''
    _name = 'cy.order.item'
    _description = '''订单条目'''

    order_id = fields.Many2one('cy.order', string='订单ID', index=True)
    qty = fields.Integer(string='购买数量', required=True)
    spu_id = fields.Integer(string='spu ID', required=True)
    skc_id = fields.Integer(string='SKC ID', required=True)
    skc_sn = fields.Char(string="货号", required=True, size=31)
    sku_id = fields.Integer(string='SKU ID', required=True)
    sku_sn = fields.Char(string='SKU SN', required=True, size=31)
    category_id = fields.Integer(string='商品分类')
    product_name = fields.Char(string='商品名称', required=True, size=255)
    product_img = fields.Char(string='商品图片', required=True, size=255)
    product_color = fields.Char(string='商品颜色', required=True, size=31)
    color_id = fields.Integer(string='颜色ID')
    product_size = fields.Char(string='商品尺寸', required=True, size=31)
    size_id = fields.Integer(string='尺寸ID')

    flashsale_id = fields.Integer(string='闪购ID')
    market_price = fields.Integer(string='市场价格')
    shop_price = fields.Integer(string='售价')
    total_promotion_deduct = fields.Integer(string='总折扣金额')

    usd_market_price = fields.Float(string='市场价格(USD)', compute="_usd_fee")
    usd_shop_price = fields.Float(string='售价(USD)', compute="_usd_fee")
    usd_total_promotion_deduct = fields.Float(string='总折扣金额(USD)', compute="_usd_fee")

    currency_market_price = fields.Float(string='市场价格', compute="_currency_fee")
    currency_shop_price = fields.Float(string='售价', compute="_currency_fee")
    currency_total_promotion_deduct = fields.Float(string='总折扣金额', compute="_currency_fee")

    def _usd_fee(self):
        conv = self.env['cy.base']
        for record in self:
            record.usd_market_price = conv.money_to_usd(record.market_price, record.order_id.currency, record.order_id.from_usd_rate)
            record.usd_shop_price = conv.money_to_usd(record.shop_price, record.order_id.currency, record.order_id.from_usd_rate)
            record.usd_total_promotion_deduct = conv.money_to_usd(record.total_promotion_deduct, record.order_id.currency, record.order_id.from_usd_rate)

    def _currency_fee(self):
        conv = self.env['cy.base']
        for record in self:
            record.currency_market_price = conv.money_int_to_float(record.market_price, record.order_id.currency)
            record.currency_shop_price = conv.money_int_to_float(record.shop_price, record.order_id.currency)
            record.currency_total_promotion_deduct = conv.money_int_to_float(record.total_promotion_deduct, record.order_id.currency)


class OrderShipping(models.Model):
    ''' cy_order_shipping '''
    _name = 'cy.order.shipping'
    _description = '''订单发货状态'''

    order_id = fields.Many2one('cy.order', string='订单ID', index=True)
    delivery_num = fields.Char(string='物流单号', required=True, size=127)
    status = fields.Selection(selection=[('1', '已发货'), ('2', '未发货'), ('3', '已取消')], default="2", size=31)

    product = fields.One2many('cy.order.shipping.product', 'shipping_id', string='物流包含商品')

    timeline = fields.One2many('cy.order.shipping.timeline', 'shipping_id', string='物流时间线')

    product_imgs = fields.Char(compute='_product_imgs', store=False, string='商品图片', size=1000)
    last_time_line = fields.Char(compute='_last_time_line', store=False, string='最近发货信息')

    @api.depends('product')
    def _product_imgs(self):
        for record in self:
            if record.product:
                images = []
                for img in record.product:
                    images.append(img.product_img)
                record.product_imgs = ",".join(images)

    @api.depends('timeline')
    def _last_time_line(self):
        for record in self:
            if record.timeline:
                record.last_time_line = record.timeline[-1].context


class ShippingTimeline(models.Model):
    _name = 'cy.order.shipping.timeline'
    _description = '''物流时间线'''
    _order = 'create_date'

    shipping_id = fields.Many2one('cy.order.shipping', string='物流ID')
    context = fields.Char(string='物流变更描述', size=255)


class ShippingProduct(models.Model):
    ''' cy_order_shipping_product '''
    _name = 'cy.order.shipping.product'
    _description = '''发货信息包含商品信息'''

    shipping_id = fields.Many2one('cy.order.shipping', string='物流ID')
    qty = fields.Integer(string='发货数量', required=True)
    product_sn = fields.Char(string='货号', required=True, size=31)
    product_name = fields.Char(string='商品名称', required=True, size=255)
    product_img = fields.Char(string='商品图片', required=True, size=1000)


class CancelOrderReason(models.Model):
    _name = 'cy.order.cancel.reason'
    _order = "sequence desc"

    reason = fields.Char(string='原因列表', size=255)
    sequence = fields.Integer(string='排序')
    active = fields.Boolean(string='是否有效')
