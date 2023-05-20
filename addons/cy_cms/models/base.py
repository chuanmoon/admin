# -*- coding: utf-8 -*-
from odoo import fields, models
from datetime import datetime


def default_end_time(*args):
    return "9999-12-30 00:00:00"


class ElementBase(models.AbstractModel):
    ''' cy_element_base model '''
    _name = 'cy.element.base'
    _description = ''' 页面元素通用属性 '''

    start_time = fields.Datetime(string='开始时间', default=fields.Datetime.now, required=True)
    end_time = fields.Datetime(string='结束时间', default=default_end_time, required=True, index=True)
    is_show = fields.Boolean(string='是否显示', default=True, required=True, index=True, copy=False)
    sequence = fields.Integer(string='排序', index=True)


class ElementEmailBase(models.AbstractModel):
    ''' cy_element_email_base model '''
    _name = 'cy.element.email.base'
    _inherit = 'cy.mail.thread'
    _description = ''' 页面元素通用属性 '''

    start_time = fields.Datetime(string='开始时间', default=fields.Datetime.now, tracking=True, required=True)
    end_time = fields.Datetime(string='结束时间', default=default_end_time, tracking=True, required=True, index=True)
