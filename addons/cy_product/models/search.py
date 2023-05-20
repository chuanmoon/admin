from odoo import fields, models


class SearchRecommend(models.Model):
    _name = 'cy.product.search.recommend'
    _order = 'sequence'
    _inherit = 'cy.mail.thread'
    _description = '''搜索推荐'''

    name = fields.Char(string="推荐名称", required=True, tracking=True, size=63)
    display_name = fields.Char(string='显示名称', required=True, tracking=True, size=63)
    header_image = fields.Char(string='头部图片', tracking=True, size=255)
    sequence = fields.Integer(string='排序', tracking=True, default=0)
    is_show = fields.Boolean(string='是否显示', tracking=True, default=True)
    action_id = fields.Many2one('cy.action', string='跳转类型', index=True)
