# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Setting(models.Model):
    ''' 活动配置 '''
    _name = 'cy.setting'
    _order = 'id'
    _description = ''' 活动配置 '''

    name = fields.Char(string='参数名', readonly=True, size=63)
    code = fields.Char(string='参数代号', readonly=True, index=True, size=63)
    property_type = fields.Selection([('text', '文本'), ('image', '图片')], string='值类型', readonly=True, size=31)
    value = fields.Char(string='参数值', size=255)
    text_value = fields.Char(string='文本', compute='_compute_text_value', inverse='_inverse_value')
    image_value = fields.Char(string='图片', compute='_compute_image_value', inverse='_inverse_value')

    @api.depends('value')
    def _compute_text_value(self):
        for rec in self:
            rec.text_value = rec.value

    @api.depends('value')
    def _compute_image_value(self):
        for rec in self:
            rec.image_value = rec.value

    def _inverse_value(self):
        pass

    @api.model
    def create(self, vals):
        property_type = vals.get('property_type', 0)
        if property_type == 'text':
            vals['value'] = vals.get('text_value', False)
        if property_type == 'image':
            vals['value'] = vals.get('image_value', False)
        return super(Setting, self).create(vals)

    def write(self, vals):
        if 'text_value' not in vals and 'image_value' not in vals:
            return super(Setting, self).write(vals)

        property_type = vals.get('property_type', False) or self.property_type
        new_value = False
        if property_type == 'text':
            new_value = vals.get('text_value', False)
        if property_type == 'image':
            new_value = vals.get('image_value', False)
        vals['value'] = new_value
        return super(Setting, self).write(vals)
