# -*- coding: utf-8 -*-
from odoo import fields, models


class ImageInfo(models.Model):
    ''' cy_image_info model '''
    _name = 'cy.image.info'
    _sql_constraints = [('url_unique', 'UNIQUE(url)', 'url不可重复')]

    url = fields.Char(string='名称', size=255)
    image_h = fields.Integer(string='高(px)')
    image_w = fields.Integer(string='宽(px)')
