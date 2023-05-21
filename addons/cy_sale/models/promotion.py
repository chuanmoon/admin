# -*- coding: utf-8 -*-
from odoo import api, fields, models, exceptions, tools
from datetime import datetime
from datetime import timedelta


def default_end_time(*args):
    return fields.Datetime.now()+timedelta(days=14)


promotion_type_priority = {
    'order_amount_discount_amount': 100,  # '订单满减(如：全场满$199减$20)'
    'order_amount_discount_rate': 200,  # '订单满折(如：全场满$199打98折)'
    'order_qty_discount_amount': 300,  # '订单满件减(如：全场买3件减$20)'
    'order_qty_discount_rate': 400,  # '订单满件折(如：全场买3件打98折)'
    'product_amount_discount_amount': 500,  # '指定商品满减(如：鞋子专场满$199减$20)'
    'product_amount_discount_rate': 600,  # '指定商品满折(如：鞋子专场满$199打98折)'
    'product_qty_discount_amount': 700,  # '指定商品满件减(如：鞋子专场买3件减$20)'
    'product_qty_discount_rate': 800,  # '指定商品满件折(如：鞋子专场买3件打98折)'
    'product_qty_discount_to_amount': 900,  # '指定商品满件减至(如：鞋子专场$9.9得3件)'
    'order_amount_free_shipping': 1000,  # '订单满金额免邮费(如：全场满$199免邮费)'
}


class Promotion(models.Model):
    ''' cy_promotion 促销规则 '''
    _name = 'cy.promotion'
    _inherit = 'cy.mail.thread'
    _order = 'id desc'

    name = fields.Char(string='促销名称', tracking=True, required=True, size=63)
    user_groups = fields.Many2many('cy.user.group', string='用户组', required=True)
    mark_text = fields.Char(string='角标文本', tracking=True, size=31)
    start_time = fields.Datetime(string='开始时间', tracking=True, default=fields.Datetime.now, required=True)
    end_time = fields.Datetime(string='结束时间', tracking=True, default=default_end_time, required=True, index=True)
    state = fields.Char(string='状态', compute='_compute_state', store=False)
    active = fields.Boolean(string='是否可用', tracking=True, default=True, index=True, required=True)
    is_can_step = fields.Boolean(string='是否可以阶梯优惠', tracking=True, default=False, required=True)
    promotion_type = fields.Selection(string='促销类型', tracking=True, selection=[
        ('order_amount_discount_amount', '订单满减(如：全场满$199减$20)'),
        ('order_amount_discount_rate', '订单满折(如：全场满$199打98折)'),
        ('order_qty_discount_amount', '订单满件减(如：全场买3件减$20)'),
        ('order_qty_discount_rate', '订单满件折(如：全场买3件打98折)'),
        ('product_amount_discount_amount', '指定商品满减(如：鞋子专场满$199减$20)'),
        ('product_amount_discount_rate', '指定商品满折(如：鞋子专场满$199打98折)'),
        ('product_qty_discount_amount', '指定商品满件减(如：鞋子专场买3件减$20)'),
        ('product_qty_discount_rate', '指定商品满件折(如：鞋子专场买3件打98折)'),
        ('product_qty_discount_to_amount', '指定商品满件减至(如：鞋子专场$9.9得3件)'),
        ('order_amount_free_shipping', '订单满金额免邮费(如：全场满$199免邮费)'),
    ], index=True,  required=True, size=31)
    priority = fields.Integer(string='优先级', compute='_compute_priority', store=True, index=True)
    amount = fields.Float(string='条件金额(USD)', tracking=True, default=2000)
    qty = fields.Integer(string='条件数量', tracking=True, default=0)
    collection_id = fields.Many2one('cy.goods.collection', tracking=True, string='条件商品系列', index=True)
    discount_amount = fields.Float(string='金额(USD)', tracking=True, default=0)
    discount_rate = fields.Integer(string='折扣(如9折输入90)', tracking=True, default=100)
    is_auto_apply = fields.Boolean(string='是否自动应用', tracking=True, default=False)

    @api.depends('start_time', 'end_time')
    def _compute_state(self):
        for record in self:
            if not record.start_time or not record.end_time:
                record.state = '待开始'
            elif datetime.now() < record.start_time:
                record.state = '待开始'
            elif datetime.now() < record.end_time:
                record.state = '进行中'
            else:
                record.state = '已结束'

    @api.depends('promotion_type')
    def _compute_priority(self):
        for record in self:
            record.priority = promotion_type_priority.get(record.promotion_type, 100000)

    @api.constrains('discount_rate')
    def _check_discount_rate(self):
        if self.discount_rate > 100 or self.discount_rate < 0:
            raise exceptions.ValidationError('折扣(如9折输入90): 输入0-100的数字.')

    def apply_now(self):
        for record in self:
            inside_gateway_link = tools.config.get('inside_gateway_link', 'http://172.17.0.1:9000/gateway')
            data = {
                'subj': 'odoo_setting_release',
                'table': 'cy_promotion',
                'id': str(record.id),
            }
            result = self.env['cy.base'].request_has_sign(inside_gateway_link+'/publish', data)
            print(result)
