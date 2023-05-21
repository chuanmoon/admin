from odoo import api, fields, models, tools
import json


def default_end_time(*args):
    return "9999-12-30 00:00:00"


class Collection(models.Model):
    ''' cy_cms_collection 产品系列'''
    _name = 'cy.cms.collection'
    _inherit = 'cy.mail.thread'
    _description = '''产品系列'''

    name = fields.Char(string="表达式名称", required=True, size=31)
    condition = fields.Text(string="表达式", required=True)
    active = fields.Boolean(string="是否有效", default=True)
    order_type = fields.Selection(selection=[("sellingScore", "Hot"), ("newScore", "New")], default="sellingScore", size=31)
    banners = fields.One2many('cy.cms.collection.banner', 'collection_id', string="banner配置")
    top_product = fields.Text(string='置顶商品', default='')

    def action_release_collection(self):
        inside_gateway_link = tools.config.get('inside_gateway_link', 'http://172.17.0.1:9000/gateway')
        for record in self:
            bizContent = {
                'collectionId': record.id,
            }
            data = {
                'module': 'cms',
                'version': '2.0',
                'method': 'CmsApi.ReloadCollection',
                'bizContent': json.dumps(bizContent)
            }
            result = self.env['cy.base'].request_has_sign(inside_gateway_link, data)
            print(result)

            if result and result.get('errorCode', 5001) == 0:
                record.message_post(body='发布成功')
            else:
                record.message_post(body='发布失败，'+result.get('errorMsg', ''))

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
    _name = 'cy.cms.collection.banner'

    collection_id = fields.Many2one('cy.cms.collection', string='商品集合')
    images = fields.Char(string="图片", required=True, size=1000)

    start_time = fields.Datetime(string='开始时间', default=fields.Datetime.now, required=True)
    end_time = fields.Datetime(string='结束时间', default=default_end_time, required=True, index=True)
    is_show = fields.Boolean(string='是否显示', default=True, required=True, index=True, copy=False)
    sequence = fields.Integer(string='排序', index=True)
