from odoo import models, fields, api


class ProductCategory(models.Model):
    _name = 'cy.product.category'
    _inherit = 'cy.mail.thread'
    _description = '''商品分类'''
    _order = 'sequence'

    name = fields.Char(string="分类名称", tracking=True, size=255)
    full_name = fields.Char(compute="_full_name", string="全称", store=False, size=255)
    parent_id = fields.Many2one('cy.product.category', index=True, string="父级别", ondelete='cascade')
    sequence = fields.Integer(string="排序", tracking=True)
    children = fields.One2many('cy.product.category', 'parent_id', string='子分类')
    active = fields.Boolean(string='是否有效', default=True, tracking=True)
    variants = fields.One2many('cy.product.category.variant', 'category_id', string="变体属性列表")
    is_show_variant_inlist = fields.Boolean(string='是否在列表页显示第一层变体', default=False, tracking=True)

    @api.depends('name', 'parent_id.full_name')
    def _full_name(self):
        for category in self:
            if category.parent_id:
                category.full_name = '%s / %s' % (category.parent_id.full_name, category.name)
            else:
                category.full_name = category.name

                
class ProductCategoryVariant(models.Model):
    _name = 'cy.product.category.variant'
    _description = '''品类变体属性定义'''
    _order = 'sequence'

    category_id = fields.Many2one('cy.product.category', string="分类", index=True)
    name = fields.Char(string="属性名称", size=255)
    select_values = fields.One2many('cy.product.category.variant.value', 'variant_id', string="属性值列表")
    active = fields.Boolean(string="是否有效", default=True, index=True)
    sequence = fields.Integer(string="排序", index=True)


class ProductCategoryVariantValue(models.Model):
    _name = 'cy.product.category.variant.value'
    _description = '''品类变体属性值定义'''
    _order = 'sequence'

    variant_id = fields.Many2one('cy.product.category.variant', string="属性", index=True)
    name = fields.Char(string="属性值", size=255)
    active = fields.Boolean(string="是否有效", default=True, index=True)
    image_url = fields.Char(string="图片地址", size=255)
    sequence = fields.Integer(string="排序", index=True)


