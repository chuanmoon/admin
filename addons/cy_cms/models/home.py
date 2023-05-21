# -*- coding: utf-8 -*-
from odoo import fields, models, api, tools
import json


class Home(models.Model):
    ''' cy_home model'''
    _name = 'cy.home'
    _inherit = 'cy.mail.thread'
    _order = 'sequence'
    _description = '首页'

    name = fields.Char(string='名称', size=63)
    page_id = fields.Many2one('cy.page', string='页面', index=True)
    active = fields.Boolean(string='是否生效', default=True, tracking=True, required=True, index=True)
    sequence = fields.Integer(string='排序', index=True)
    navs = fields.One2many('cy.nav', 'home_id', '导航')

    def action_release_home(self):
        inside_gateway_link = tools.config.get('inside_gateway_link', 'http://172.17.0.1:9000/gateway')
        for record in self:
            bizContent = {
                'homeId': record.id,
            }
            data = {
                'module': 'cms',
                'version': '2.0',
                'method': 'CmsApi.HomeRelease',
                'bizContent': json.dumps(bizContent)
            }
            result = self.env['cy.base'].request_has_sign(inside_gateway_link, data)
            print(result)

            if result and result.get('errorCode', 5001) == 0:
                record.message_post(body='首页发布成功')
            else:
                record.message_post(body='首页发布失败，'+result.get('errorMsg', ''))
