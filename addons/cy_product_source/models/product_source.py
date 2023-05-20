from odoo import models, fields


class ProductSource(models.Model):
    ''' cy_product_source '''
    _name = 'cy.product.source'
    _description = '商品来源'
    _log_access = False
    _order = 'id desc'

    _sql_constraints = [('url_unique', 'UNIQUE(url)', '来源地址不能重复！')]

    name = fields.Char(string='商品名称', index=True, size=255)
    channel = fields.Char(string='渠道', size=31)
    images = fields.Char(string='商品图片', size=10000)
    url = fields.Char(string='来源地址', size=255)
    spu_id = fields.Many2one('cy.product.spu', string='商品SPU')
    content = fields.Text(string='内容')
