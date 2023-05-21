from odoo import models, fields, api


class ProductCategory(models.Model):
    ''' cy_product_category 商品分类 '''
    _name = 'cy.product.category'
    _inherit = 'cy.mail.thread'
    _description = '''商品分类'''
    _order = 'sequence'

    name = fields.Char(string="分类名称", tracking=True, size=255)
    full_name = fields.Char(compute="_full_name", string="全称", store=False, size=255)
    parent_id = fields.Many2one('cy.product.category', index=True, string="父级别", ondelete='cascade')
    children = fields.One2many('cy.product.category', 'parent_id', string='子分类')
    is_show_variant_inlist = fields.Boolean(string='商品列表显示变体', default=False, tracking=True, help="商品列表显示第一级变体，比如：颜色")
    sequence = fields.Integer(string="排序", tracking=True)
    active = fields.Boolean(string='是否有效', default=True, tracking=True)
    variants = fields.One2many('cy.product.category.variant.rel', 'category_id', string="变体属性列表")
    attrs = fields.One2many('cy.product.category.attr.rel', 'category_id', string="普通属性列表")

    @api.depends('name', 'parent_id.full_name')
    def _full_name(self):
        for category in self:
            if category.parent_id:
                category.full_name = '%s / %s' % (category.parent_id.full_name, category.name)
            else:
                category.full_name = category.name



