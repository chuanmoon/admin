from odoo import models, fields, api


class ProductCategory(models.Model):
    _name = 'cy.product.category'
    _inherit = 'cy.mail.thread'
    _description = '''
        商品分类
    '''
    _rec_name = "display_name"
    _order = 'sequence'

    name = fields.Char(string="分类名称", tracking=True, size=255)
    code = fields.Char(string='分类代码', size=15)

    display_name = fields.Char(string="英文名", tracking=True, size=255)

    full_name = fields.Char(compute="_full_name", string="全称", store=False, size=255)
    display_full_name = fields.Char(compute="_display_full_name", string="显示全称", store=False, size=255)

    parent_id = fields.Many2one('cy.product.category', index=True, string="父级别", ondelete='cascade')
    sequence = fields.Integer(string="排序", tracking=True)
    children = fields.One2many('cy.product.category', 'parent_id', string='子分类')

    active = fields.Boolean(string='是否有效', default=True, tracking=True)

    size_image = fields.Char(string="尺寸信息图片", tracking=True, size=255)

    # size_guide_id = fields.Many2one('cy.product.size.group', string="尺寸组")

    @api.depends('name', 'parent_id.full_name')
    def _full_name(self):
        for category in self:
            if category.parent_id:
                category.full_name = '%s / %s' % (category.parent_id.full_name, category.name)
            else:
                category.full_name = category.name

    @api.depends('display_name', 'parent_id.display_full_name')
    def _display_full_name(self):
        for category in self:
            if category.parent_id:
                category.display_full_name = '%s / %s' % (category.parent_id.display_full_name, category.display_name)
            else:
                category.display_full_name = category.display_name
