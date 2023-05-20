# -*- coding: utf-8 -*-
from odoo import fields, models, api


class Popup(models.Model):
    ''' cy_popup model'''
    _name = 'cy.popup'
    _inherit = 'cy.element.email.base'
    _order = 'sequence'
    _description = '弹框'

    name = fields.Char(string='名字', index=True, size=63)
    image_url = fields.Char(string='图片', tracking=True, required=True, size=255)
    pc_image_url = fields.Char(string='PC端图片', tracking=True, required=True, size=255)
    user_groups = fields.Many2many('cy.user.group', string='用户组', required=True)
    is_repeat = fields.Boolean(string='是否重复', required=True)
    interval_hours = fields.Integer(string='间隔小时数', required=True, default=1)
    sequence = fields.Integer(string='排序', index=True)
    active = fields.Boolean(string='是否生效', default=True, required=True, index=True)
