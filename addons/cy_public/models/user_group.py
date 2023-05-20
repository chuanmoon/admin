# -*- coding: utf-8 -*-
from odoo import fields, models, api, tools


class UserGroup(models.Model):
    ''' cy_user_group 用户组'''
    _name = 'cy.user.group'
    _description = ''' 用户组 '''

    name = fields.Char(string='分组名称', size=63, required=True)
    new_old_range = fields.Selection([('all', '所有用户'), ('new_7days', '7天内新客'), ('new', '新客'), ('old', '老客')], string='新老客范围', required=True, default='all', size=31)
    login_status = fields.Selection([('all', '所有状态'), ('not_login', '未登录'), ('login', '已登录')], string='登录状态', required=True, default='all', size=31)
    active = fields.Boolean(string='是否可用', default=True)

    def apply_now(self):
        for record in self:
            inside_gateway_link = tools.config.get('inside_gateway_link', 'http://172.17.0.1:9000/gateway')
            data = {
                'subj': 'odoo_setting_release',
                'table': 'cy_user_group',
                'id': str(record.id),
            }
            result = self.env['cy.public'].request_has_sign(inside_gateway_link+'/publish', data)
            print(result)
