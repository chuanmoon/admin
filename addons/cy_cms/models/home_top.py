# -*- coding: utf-8 -*-
from odoo import fields, models, tools
import json


class HomeTop(models.Model):
    ''' cy_home_top model'''
    _name = 'cy.home.top'
    _inherit = 'cy.element.email.base'
    _order = 'sequence'
    _description = 'WEB顶部图片'

    name = fields.Char(string='名称', size=63)
    pc_image_url = fields.Char(string='PC图片', size=255, tracking=True)
    m_image_url = fields.Char(string='M图片', size=255, tracking=True)
    active = fields.Boolean(string='是否生效', default=True, tracking=True, required=True, index=True)
    sequence = fields.Integer(string='排序', index=True)
    action = fields.Many2one('cy.action', string='点击动作', index=True)
    has_count_down = fields.Boolean(string='是否显示倒计时')

    def action_release_home_top(self):
        inside_gateway_link = tools.config.get('inside_gateway_link', 'http://172.17.0.1:9000/gateway')
        for record in self:
            data = {
                'module': 'cms',
                'version': '2.0',
                'method': 'CmsApi.HomeTopRelease',
                'bizContent': '{}'
            }
            result = self.env['cy.base'].request_has_sign(inside_gateway_link, data)

            if result and result.get('errorCode', 5001) == 0:
                record.message_post(body='WEB页面顶部图片发布成功')
            else:
                record.message_post(body='WEB页面顶部图片发布失败，'+result.get('errorMsg', ''))
