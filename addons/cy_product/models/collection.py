from odoo import api, fields, models, tools
import json


def default_end_time(*args):
    return "9999-12-30 00:00:00"


class Collection(models.Model):
    ''' cy_goods_collection 商品系列'''
    _name = 'cy.goods.collection'
    _inherit = 'cy.mail.thread'
    _description = '''商品系列'''

    name = fields.Char(string="表达式名称", required=True, size=31)
    condition = fields.Text(string="表达式", required=True)
    active = fields.Boolean(string="是否有效", default=True)
    order_type = fields.Selection(selection=[("sellingScore", "Hot"), ("newScore", "New")], default="sellingScore", size=31)
    banners = fields.One2many('cy.goods.collection.banner', 'collection_id', string="banner配置")
    top_product = fields.Text(string='置顶商品', default='')

    @api.model_create_multi
    def create(self, vals_list):
        result = super(Collection, self).create(vals_list)
        for record in result:
            self.env['cy.action'].sync_action(record.name, 'collection', str(record.id))
        return result

    def write(self, vals):
        result = super(Collection, self).write(vals)
        for record in self:
            self.env['cy.action'].sync_action(record.name, 'collection', str(record.id))
        return result


class CollectionBanner(models.Model):
    ''' cy_goods_collection_banner 商品系列banner'''
    _name = 'cy.goods.collection.banner'

    collection_id = fields.Many2one('cy.goods.collection', string='商品系列')
    images = fields.Char(string="图片", required=True, size=1023)
    start_time = fields.Datetime(string='开始时间', default=fields.Datetime.now, required=True)
    end_time = fields.Datetime(string='结束时间', default=default_end_time, required=True, index=True)
    is_show = fields.Boolean(string='是否显示', default=True, required=True, index=True, copy=False)
    sequence = fields.Integer(string='排序', index=True)
