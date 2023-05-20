from odoo import fields, models, api
import json


class PTSPU(models.Model):
    _name = 'cy.product.spu'
    _rec_name = "spu_sn"
    _inherit = 'cy.mail.thread'
    _sql_constraints = [('spu_sn_unique', 'UNIQUE(spu_sn)', 'spu_sn不可重复')]
    _description = '''
        SPU 全称为 Standard Product Unit，译为标准化产品单元。是商品信息聚合的最小单位，是一组可复用、易检索的标准化信息的集合，该集合描述了一个产品的特性。通俗点讲，属性值、特性相同的商品就可以称为一个 SPU。
    '''

    category_id = fields.Many2one('cy.product.category', string="分类", index=True)
    spu_sn = fields.Char(string="SPU 序号", size=31)  # product_sn_prefix
    skcs = fields.One2many('cy.product.skc', 'spu_id', string='skc列表')
    skc_count = fields.Integer(compute="_compute_skc_count", store=False, string="skc数量")
    active = fields.Boolean(string="是否有效", default=True, tracking=True, index=True)

    @api.depends("skcs")
    def _compute_skc_count(self):
        for record in self:
            record.skc_count = len(record.skcs)

    @api.model_create_multi
    def create(self, vals_list):
        result = super(PTSPU, self).create(vals_list)
        if result.id:
            result.write({'spu_sn': 'P%010d' % result.id})
        return result


class PTSKC(models.Model):
    _name = 'cy.product.skc'
    _rec_name = "skc_sn"
    _inherit = 'cy.mail.thread'
    _description = '''
        商品属性单元
    '''
    spu_id = fields.Many2one('cy.product.spu', string="spu ID", ondelete="cascade", index=True)
    category_id = fields.Many2one('cy.product.category', string="分类", index=True)
    skc_sn = fields.Char(string="skc sn", size=31, index=True)  # TODO 实现生成函数 #product_sn
    name = fields.Char(string="商品名称", size=255)
    name_zh = fields.Char(string="商品中文名称", size=255)
    dispaly_name = fields.Char(compute="_display_name", string="展示名称", store=False)
    image_urls = fields.Char(string='商品图片', tracking=True, size=2047)
    info = fields.Char(string="商品信息", tracking=True, size=1023)
    sku_count = fields.Integer(compute="_sku_count", store=False, string="sku数量")

    skus = fields.One2many('cy.product.sku', 'skc_id', string='sku列表')

    oms_market_price = fields.Float(string="市场价", default=0.00)
    oms_shop_price = fields.Float(string='售价', default=0.00)
    market_price = fields.Float(compute="_market_price", string='划线价格', store=False)
    shop_price = fields.Float(compute='_shop_price', string='基础售价')

    prices = fields.One2many('cy.product.price', 'skc_id', string='价格', tracking=True)

    color_id = fields.Many2one('cy.product.color', string="商品颜色", index=True)
    select_color_img = fields.Char(string="点选的色球图片", size=255)
    color_img = fields.Char(compute="_color_image", string="颜色图片", store=False)
    color_img_list = fields.Char(compute="_color_img_list", string="颜色图片", store=False)
    active = fields.Boolean(string="是否生效", default=True, tracking=True, index=True)
    attributes = fields.One2many('cy.product.attribute', 'skc_id', string="商品属性")
    tag = fields.Selection(selection=[('hot', 'hot'), ('new', 'new'), ('sale', 'sale')], size=31)

    limit_qty = fields.Integer(string="购买上限数量(0 不限购)", default=1000)

    publish_time = fields.Datetime(string='最新上架时间')
    first_shelf_time = fields.Datetime(string='首次上架时间')

    @api.depends('oms_market_price', 'oms_shop_price')
    def _market_price(self):
        for record in self:
            if record.oms_market_price:
                record.market_price = record.oms_market_price
            else:
                record.market_price = 0

    # TODO uncomplate

    @api.depends('oms_shop_price')
    def _shop_price(self):
        for record in self:
            record.shop_price = record.oms_shop_price

    @api.depends("skus")
    def _sku_count(self):
        for record in self:
            record.sku_count = len(record.skus)

    @api.depends("color_id")
    def _color_img_list(self):
        for record in self:
            color_img = ''
            if record.color_id:
                color_img = record.color_id.color_img
            if record.select_color_img:
                color_img = record.select_color_img
            record.color_img_list = color_img

    @api.depends("color_id")
    def _color_image(self):
        for record in self:
            color_img = ''
            if record.color_id:
                color_img = record.color_id.color_img
            if record.select_color_img:
                color_img = record.select_color_img

            if record.image_urls:
                record.color_img = '''<div style="display:flex;align-items:flex-end;gap:20px;background:#f0eeee;border:1px solid #CCC;padding:4px;border-radius:3px;">
                    <img src="https://img.your_domin.com/%(color_img)s"></img>
                    <button class="btn oe_read_only o_iframe_button" url="/cy_product/static/src/html/select_color_image.html?v=1&skc_id=%(skc_id)s&image=%(image)s">从商品主图点选色球</button>
                </div>''' % {'color_img': color_img, 'skc_id': record.id, 'image': record.image_urls.split(',')[0]}
            else:
                record.color_img = '''<div><img src="https://img.your_domin.com/%(color_img)s"></img></div>''' % {'color_img': color_img}

    @api.depends("name", "skc_sn")
    def _display_name(self):
        for record in self:
            if record.skc_sn and record.name:
                record.display_name = "[%s]%s/%s" % (record.skc_sn, record.name, record.color_id.name)
            else:
                record.display_name = record.name

    @api.model_create_multi
    def create(self, vals_list):
        result = super(PTSKC, self).create(vals_list)
        if result.id:
            result.write({'skc_sn': 'C%010d' % result.id})
        return result


class PTSKU(models.Model):
    _name = 'cy.product.sku'
    _inherit = 'cy.mail.thread'
    _description = '''
        商品库存价格单元
    '''
    _rec_name = "name"

    name = fields.Char(compute="_product_name", string="商品名称", store=False)

    skc_id = fields.Many2one('cy.product.skc', string="skc ID", index=True)
    spu_id = fields.Many2one(compute='_compute_spu_id', comodel_name='cy.product.spu', string="spu id", store=True, index=True)

    sku_sn = fields.Char(string='sku 序号', size=31, index=True)  # TODO 实现生成函数
    size_id = fields.Many2one('cy.product.size', string='商品尺寸', ondelete='set null', index=True)
    stock = fields.One2many('cy.product.stock', 'sku_id', string='库存', tracking=True)
    active = fields.Boolean(string="是否有效", default=True, tracking=True, index=True)

    @api.depends('skc_id')
    def _compute_spu_id(self):
        for record in self:
            if record.skc_id:
                record.spu_id = record.skc_id.spu_id
            else:
                record.spu_id = 0

    @api.depends("skc_id")
    def _product_name(self):
        for record in self:
            record.name = "%s/%s" % (record.skc_id.display_name, record.size_id.value)

    @api.model_create_multi
    def create(self, vals_list):
        result = super(PTSKU, self).create(vals_list)
        if result.id:
            result.write({'sku_sn': 'K%010d' % result.id})
        return result


class ProductStock(models.Model):
    _name = 'cy.product.stock'
    _description = '''商品库存'''
    _inherit = 'cy.mail.thread'
    _sql_constraints = [('sku_id_unique', 'UNIQUE(sku_id)', 'sku_id不可重复')]
    _rec_name = "stock"

    sku_id = fields.Many2one('cy.product.sku', string='商品SKU')
    stock = fields.Integer(string='库存数量', tracking=True)


class ProductPrice(models.Model):
    _name = 'cy.product.price'
    _description = '''商品价格'''
    _inherit = 'cy.mail.thread'
    _sort = 'sequence'
    _rec_name = "shop_price"

    skc_id = fields.Many2one('cy.product.skc', string='商品SKc', index=True, ondelete='cascade')
    shop_price = fields.Float(string='商品价格(美元)', tracking=True)
    start_time = fields.Datetime(string='开始时间', default=fields.Datetime.now, required=True, tracking=True)
    end_time = fields.Datetime(string='结束时间', required=True, index=True, tracking=True)
    active = fields.Boolean(string="是否生效", default=True, tracking=True, index=True)
    sequence = fields.Integer(string='优先级', tracking=True)


class ProductColor(models.Model):
    _name = 'cy.product.color'
    _rec_name = "name"
    _order = 'sequence'
    _description = '''
        商品颜色
    '''
    name = fields.Char(string='颜色名称', size=31)
    display_name = fields.Char(string="英文名称", size=31)
    color_img = fields.Char(string="颜色图片", size=255)
    color_rgb = fields.Char(string="颜色色号", size=31)
    active = fields.Boolean(string="是否可用", default=True, index=True)

    parent_id = fields.Integer(string='父级ID', default=0)

    is_in_filter = fields.Boolean(string='显示在筛选项中', default=False)
    is_default_in_filter = fields.Boolean(string='在筛选项中优先显示', default=False)
    sequence = fields.Integer(string='排序')


class ProductAttribute(models.Model):
    _name = 'cy.product.attribute'
    _sql_constraints = [('skc_id_unique', 'UNIQUE(skc_id)', 'skc_id不可重复')]
    _description = '''
        商品属性
    '''
    skc_id = fields.Integer(string="商品SKC")
    attrs = fields.Text(string="属性列表")
    attributes = fields.One2many(string="属性列表", compute='_attributes')

    @api.depends("attrs")
    def _attributes(self):
        self.attributes = json.loads(self.attrs)


class ProductSize(models.Model):
    _name = 'cy.product.size'
    _description = '''商品尺寸'''
    _order = 'sequence'
    _rec_name = "value"

    is_in_filter = fields.Boolean(string='显示在筛选项中', default=False)
    is_default_in_filter = fields.Boolean(string='在筛选项中默认显示', default=False)
    sequence = fields.Integer(string="排序")
    value = fields.Char(string="尺寸名称", size=31)
    code = fields.Char(string="size 编码", size=31)

    active = fields.Boolean(string='是否生效', index=True)
