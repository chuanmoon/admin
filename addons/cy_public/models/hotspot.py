# -*- coding: utf-8 -*-
from odoo import fields, models


class Hotspot(models.Model):
    _name = 'cy.hotspot'

    name = fields.Char(string='名字', size=31)
    action_id = fields.Many2one('cy.action', string='跳转类型', index=True)
    image_id = fields.Many2one('cy.image.info', string='图片', index=True)
    x = fields.Integer(string='坐标x')
    y = fields.Integer(string='坐标y')
    w = fields.Integer(string='坐标宽度')
    h = fields.Integer(string='坐标高度')
