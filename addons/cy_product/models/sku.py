from odoo import fields, models, api


class Sku(models.Model):
    ''' cy_product_sku 商品SKU '''
    _name = 'cy.product.sku'
    _rec_name = "sku_sn"
    _inherit = 'cy.mail.thread'
    _sql_constraints = [('sku_sn_unique', 'UNIQUE(sku_sn)', 'sku_sn不可重复')]
    _description = '''Stock Keeping Unit'''

    spu_id = fields.Many2one('cy.product.spu', string="SPU ID", ondelete="cascade", index=True)
    sku_sn = fields.Char(string="SKU SN", size=31, index=True)
    name = fields.Char(string="商品名称", size=255)
    image_urls = fields.Char(string='商品图片', tracking=True, size=2047)
    info = fields.Char(string="商品信息", tracking=True, size=1023)
    cost_price = fields.Float(string='成本价格(CNY)')
    market_price = fields.Float(string='划线价格(CNY)')
    shop_price = fields.Float(string='基础售价(CNY)')
    weight = fields.Float(string='重量(克)')
    volume = fields.Float(string='体积(平方厘米)')
    active = fields.Boolean(string="是否生效", default=True, tracking=True, index=True)
    limit_qty = fields.Integer(string="购买上限数量(0 不限购)", default=0)
    last_publish_time = fields.Datetime(string='最新上架时间')
    first_publish_time = fields.Datetime(string='首次上架时间')

    stock = fields.One2many('cy.product.stock', 'sku_id', string='库存', tracking=True)
    variants = fields.One2many('cy.product.variant', 'sku_id', string="变体属性")
    attrs = fields.One2many('cy.product.attr', 'sku_id', string="常规属性")
    detail = fields.One2many('cy.product.detail', 'sku_id', string="商品详情")

    @api.model_create_multi
    def create(self, vals_list):
        result = super(Sku, self).create(vals_list)
        if result.id:
            result.write({'sku_sn': 'SKU%010d' % result.id})
        return result


class ProductStock(models.Model):
    ''' cy_product_stock 商品库存 '''
    _name = 'cy.product.stock'
    _description = '''商品库存'''
    _inherit = 'cy.mail.thread'
    _sql_constraints = [('sku_id_unique', 'UNIQUE(sku_id)', 'sku_id不可重复')]
    _rec_name = "stock"

    sku_id = fields.Many2one('cy.product.sku', string='商品SKU')
    stock = fields.Integer(string='库存数量', tracking=True)


class ProductVariant(models.Model):
    ''' cy_product_variant 商品变体属性 '''
    _name = 'cy.product.variant'
    _description = '''商品变体属性'''

    sku_id = fields.Many2one('cy.product.sku', string='商品SKU', ondelete="cascade", index=True)
    variant_id = fields.Many2one('cy.product.category.variant', string="变体属性", index=True)
    variant_value_id = fields.Many2one('cy.product.category.variant.value', string="变体属性值", index=True)
    variant_image_url = fields.Char(string="变体小图片", size=255, help="变体属性值对应的小图片, 覆盖公用图片, 只有当前商品列表和详情页展示")


class ProductAttr(models.Model):
    ''' cy_product_attr 商品常规属性 '''
    _name = 'cy.product.attr'
    _description = '''商品常规属性'''
    _order = 'sequence'

    sku_id = fields.Many2one('cy.product.sku', string='商品SKU', ondelete="cascade", index=True)
    attr_id = fields.Many2one('cy.product.category.attr', string="属性", index=True)
    attr_value = fields.Char(string="属性值", size=255)


class ProductDetail(models.Model):
    ''' cy_product_detail 商品详情 '''
    _name = 'cy.product.detail'
    _description = '''商品详情'''

    sku_id = fields.Many2one('cy.product.sku', string='商品SKU', ondelete="cascade", index=True)
    row_type = fields.Selection([('text', '文本'), ('image', '图片')], string="行类型", default='text')
    text_value = fields.Char(string="行文本", size=2047)
    image_urls = fields.Char(string="行图片", size=2047)
    sequence = fields.Integer(string="排序", default=0, index=True)
