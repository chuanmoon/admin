# -*- coding: utf-8 -*-
from odoo import fields, models


class Wishlist(models.Model):
    ''' cy_wishlist 心愿单 '''
    _name = 'cy.wishlist'
    _order = 'id desc'
    _log_access = False

    user_id = fields.Integer(string='用户ID', index=True)
    skc_id = fields.Integer(string='skc id', index=True)
    write_date = fields.Datetime(string='写入时间')
