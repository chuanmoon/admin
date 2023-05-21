# -*- coding: utf-8 -*-
from odoo import fields, models, api, tools


class Platform(models.Model):
    _name = 'cy.platform'
    _log_access = False

    name = fields.Char(string='名称', size=15)
    code = fields.Char(string='代号', size=15)


class Lang(models.Model):
    ''' cy_lang '''
    _name = 'cy.lang'
    _description = '语言'
    _order = 'sequence'
    _log_access = False

    name = fields.Char(string='名字', index=True, size=15)
    code = fields.Char(string='google代号', index=True, help='https://cloud.google.com/translate/docs/languages?hl=zh-cn', size=15)
    active = fields.Boolean(string='是否可用', default=True, index=True)
    sequence = fields.Integer(string='排序', index=True)


class Currency(models.Model):
    ''' cy_currency '''
    _name = 'cy.currency'
    _description = '币种'
    _order = 'sequence'
    _log_access = False

    name = fields.Char(string='名字', index=True, size=15)
    code = fields.Char(string='代号', index=True, size=15)
    from_usd_rate = fields.Float(string='汇率', help='美元兑换其他币种的汇率')
    active = fields.Boolean(string='是否可用', default=True, index=True)
    sequence = fields.Integer(string='排序', index=True)

    def apply_now(self):
        for record in self:
            inside_gateway_link = tools.config.get('inside_gateway_link', 'http://172.17.0.1:9000/gateway')
            data = {
                'subj': 'odoo_setting_release',
                'table': 'cy_currency',
                'id': str(record.id),
            }
            result = self.env['cy.base'].request_has_sign(inside_gateway_link+'/publish', data)
            print(result)
