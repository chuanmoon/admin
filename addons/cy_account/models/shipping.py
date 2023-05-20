from odoo import models, fields, api, tools
from datetime import datetime


def default_end_time(*args):
    return "9999-12-30 00:00:00"


class ShippingRule(models.Model):
    ''' cy_shipping_rule '''
    _name = 'cy.shipping.rule'
    _description = '运费规则'
    _order = 'sequence'

    name = fields.Char(string='规则名', size=63)
    shipping_id = fields.Many2one('cy.shipping', string='配送方式')
    min_days = fields.Integer(string='最快天数', default=7)
    max_days = fields.Integer(string='最慢天数', default=14)
    items = fields.One2many('cy.shipping.rule.item', 'rule_id', string='明细配置')
    regions_type = fields.Selection([('all', '所有区域'), ('in', '指定区域')], default='all', size=31)
    regions = fields.Many2many('cy.region', string='区域列表')
    start_time = fields.Datetime(string='开始时间', default=fields.Datetime.now, required=True)
    end_time = fields.Datetime(string='结束时间', default=default_end_time, required=True, index=True)
    user_groups = fields.Many2many('cy.user.group', string='用户组', required=True)
    active = fields.Boolean(string='是否有效', default=True, index=True)
    sequence = fields.Integer(string='优先级', index=True)
    link = fields.Char(string='运费说明链接', size=255)

    items_result = fields.Char(string='明细结果', compute='_compute_items_result', store=False)

    @api.depends('items')
    def _compute_items_result(self):
        for record in self:
            if record.items:
                trs = ''
                min = 0
                for item in record.items:
                    osf = item.one_shipping_fee < 0.00000001 and '无' or ('%.2f' % item.one_shipping_fee)
                    trs += '<tr><td>%.2f~%.2f</td><td>%.2f</td><td>%s</td></tr>' % (min, item.max_pay_deduct, item.first_shipping_fee, osf)
                    min = item.max_pay_deduct
                trs += '<tr><td>%.2f~无限</td><td>%.2f</td><td>无</td></tr>' % (min, 0)

                record.items_result = '<style>.shipping_items_result {border-collapse: collapse;text-align: right;}.shipping_items_result th,.shipping_items_result td{border: 1px solid #CCC;padding: 6px 16px;}</style><table class="shipping_items_result"><thead><tr><th>购物车金额(USD)</th><th>首件运费(USD)</th><th>加件运费(USD)</th></tr></thead><tbody>' + \
                    trs+'</tbody></table>'
            else:
                record.items_result = ''

    def apply_now(self):
        for record in self:
            inside_gateway_link = tools.config.get('inside_gateway_link', 'http://172.17.0.1:9000/gateway')
            data = {
                'subj': 'odoo_setting_release',
                'table': 'cy_shipping_rule',
                'id': str(record.id),
            }
            result = self.env['cy.public'].request_has_sign(inside_gateway_link+'/publish', data)
            print(result)


class ShippingRuleItem(models.Model):
    ''' cy_shipping_rule_item '''
    _name = 'cy.shipping.rule.item'
    _description = '运费规则明细'
    _order = 'max_pay_deduct'

    rule_id = fields.Many2one('cy.shipping.rule', string='规则')
    max_pay_deduct = fields.Float(string='实付金额上限(USD)', default=49)
    first_shipping_fee = fields.Float(string='首件运费(USD)', default=12.99)
    one_shipping_fee = fields.Float(string='加件运费(USD)', default=0)


class Shipping(models.Model):
    ''' cy_shipping '''
    _name = 'cy.shipping'
    _description = '配送方式'
    _rec_name = 'shipping_name'
    _order = 'sequence'

    shipping_id = fields.Integer(string='OMS id')
    shipping_name = fields.Char(string='配送方式名称', size=63)
    insure = fields.Float(string='保价费用(USD)', default=1.99)
    sequence = fields.Integer(string='优先级', index=True)
    active = fields.Boolean(string='是否有效', default=True, index=True)
