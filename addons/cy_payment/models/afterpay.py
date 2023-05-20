from odoo import models, fields


class AfterpayOrder(models.Model):
    ''' cy_afterpay_order '''
    _name = "cy.afterpay.order"
    _log_access = False
    _sql_constraints = [('biz_order_on_afterpay_token_unique', 'UNIQUE(biz_order_on,afterpay_token)', 'biz_order_on,afterpay_token不可重复')]

    biz_order_on = fields.Char(string='order_on(biz)', size=63, index=True)
    biz_order_id = fields.Integer(string='order_on(biz)')
    afterpay_token = fields.Char(string='token(afterpay)', size=63, index=True)
    afterpay_order_no = fields.Char(string='order_id(afterpay)', size=63)
    create_date = fields.Datetime(string='写入时间', index=True)
    platform = fields.Char(string='平台', size=31)
    country_id = fields.Integer(string='国家ID')
    status = fields.Char(string='状态', size=31, index=True)  # DECLINED/APPROVED
    callback_success = fields.Boolean(string='是否已经通知', index=True)
