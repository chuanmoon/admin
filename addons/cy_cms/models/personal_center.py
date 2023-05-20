# -*- coding: utf-8 -*-
from odoo import fields, models, api, tools


class PersonalCenter(models.Model):
    ''' cy_personal_center model'''
    _name = 'cy.personal.center'
    _order = 'id desc'
    _description = '个人中心'
    _order = 'sequence'

    name = fields.Char(string='名称', size=63)
    top_image = fields.Char(string='顶部图片', size=255)
    rows = fields.One2many('cy.personal.center.row', 'personal_center_id', string='行')
    sequence = fields.Integer(string='优先级', index=True)


class PersonalCenterRow(models.Model):
    ''' cy_personal_center_row model'''
    _name = 'cy.personal.center.row'
    _order = 'block_no, sequence'
    _description = '个人中心行'

    personal_center_id = fields.Many2one('cy.personal.center', string='个人中心', index=True)
    icon = fields.Char(string='图标', size=255)
    name = fields.Char(string='标题', size=255)
    block_no = fields.Selection([('1', '1'), ('2', '2'), ('3', '3')], string='块序号', default='1', size=31)
    action_id = fields.Many2one('cy.action', string='点击动作', index=True)
    sequence = fields.Integer(string='优先级', index=True)
    is_show = fields.Boolean(string='是否显示', index=True, default=True)
