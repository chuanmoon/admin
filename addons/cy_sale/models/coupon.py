# -*- coding: utf-8 -*-
from operator import index
from odoo import fields, models, tools, api
from datetime import timedelta


def default_end_time(*args):
    return fields.Datetime.now()+timedelta(days=14)


class CouponRule(models.Model):
    ''' cy_coupon_rule 优惠券规则 '''
    _name = 'cy.coupon.rule'
    _inherit = 'cy.mail.thread'
    _order = 'id desc'
    _sql_constraints = [('code_unique', 'UNIQUE(code)', 'code不可重复')]
    _rec_name = 'code'

    code = fields.Char(string='兑换代码', tracking=True, required=True, size=31)
    start_time = fields.Datetime(string='开始时间', tracking=True, default=fields.Datetime.now, required=True)
    end_time = fields.Datetime(string='结束时间', tracking=True, default=default_end_time, required=True, index=True)
    days = fields.Integer(string='有效天数', tracking=True, default=7, help='从发券时间开始计算，如果比结束时间早，就以这个时间为准，否则以结束时间为准')
    total_limit = fields.Integer(string='总发券数量', tracking=True, default=999999999)
    one_user_limit = fields.Integer(string='单个用户张数', tracking=True, default=1)
    send_type = fields.Selection(string='投放方式', tracking=True, selection=[
        ('code', '直接应用券号，无需投放'),
        ('auto', '自动投放'),
        ('normal', 'API投放'),
    ], index=True,  required=True, default='code', size=31)
    promotion_id = fields.Many2one('cy.promotion', string='促销规则')

    def apply_now(self):
        for record in self:
            inside_gateway_link = tools.config.get('inside_gateway_link', 'http://172.17.0.1:9000/gateway')
            data = {
                'subj': 'odoo_setting_release',
                'table': 'cy_coupon_rule',
                'id': str(record.id),
            }
            result = self.env['cy.public'].request_has_sign(inside_gateway_link+'/publish', data)
            print(result)

    @api.onchange('code')
    def set_upper(self):
        if self.code:
            self.code = str(self.code).upper()
        else:
            self.code = ''
        return


class CouponCode(models.Model):
    ''' cy_coupon_code 用户优惠券 '''
    _name = 'cy.coupon.code'
    _order = 'id desc'
    _log_access = False

    rule_id = fields.Many2one('cy.coupon.rule', string='规则Id', index=True)
    user_id = fields.Integer(string='用户Id', index=True)
    write_date = fields.Datetime(string='写入时间', index=True)
    start_time = fields.Datetime(string='开始时间')
    end_time = fields.Datetime(string='失效时间', index=True)
    state = fields.Selection([('active', '有效的'), ('used', '已使用'), ('invalid', '无效的')], string='状态', index=True, size=31)
