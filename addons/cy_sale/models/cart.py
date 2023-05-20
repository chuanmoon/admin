# -*- coding: utf-8 -*-
from odoo import fields, models


class CartLine(models.Model):
    ''' cy_cart_line 购物车 '''
    _name = 'cy.cart.line'
    _order = 'id desc'
    _log_access = False

    owner = fields.Char(string='归属(key)', index=True, size=63)
    line_type = fields.Char(string='行类型', size=31)
    sku_id = fields.Integer(string='sku id')
    qty = fields.Integer(string='数量')
    write_date = fields.Datetime(string='写入时间')
    selected = fields.Boolean(string='是否已勾选')
    ext_info = fields.Char(string='扩展数据', size=127)
