# -*- coding: utf-8 -*-
from odoo import fields, models, api


class Action(models.Model):
    ''' cy_action model '''
    _name = 'cy.action'
    _inherit = 'cy.mail.thread'
    _description = ''' 点击动作 '''
    _sql_constraints = [('action_unique', 'UNIQUE(action_type,target_data)', 'type and data不可重复')]

    name = fields.Char(string='名称', required=True, tracking=True, index=True, size=63)
    title = fields.Char(string='标题', required=True, tracking=True, size=63)
    action_type = fields.Selection([
        ('open_search', '打开搜索页面'),
        ('open_search_keywords', '打开搜索关键字'),
        ('open_product', '打开商品详情'),
        ('open_collection', '打开商品列表'),
        ('open_page', '打开页面'),
        ('open_flashsale', '打开flashsale'),
        ('open_cart', '打开购物车'),
        ('open_coupons', '打开优惠券'),
        ('open_address_book', '打开地址簿'),
        ('open_login', '打开登录'),
        ('open_register', '打开注册'),
        ('open_link', '打开网址')
    ], string='动作', required=True, tracking=True, index=True, size=31)
    target_data = fields.Char(string='目标(id或link)', size=255, tracking=True, index=True)

    @api.onchange("target_data")
    def onchange_target_data(self):
        if not self.target_data:
            return
        self.target_data = self.target_data.strip()

    def sync_action(self, title, action_type, target_data):
        if not action_type:
            return

        title = title or ''
        target_data = target_data or ''

        target_data = target_data.strip()
        name = title+'/' + action_type+'/'+target_data
        action_type = 'open_'+action_type

        records = self.search([('action_type', '=', action_type), ('target_data', '=', target_data)])
        data = {'name': name,  'action_type': action_type, 'target_data': target_data}
        if records:
            records.write(data)
        else:
            data['title'] = title
            self.create(data)
