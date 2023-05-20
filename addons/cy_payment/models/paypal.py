from odoo import models, fields


class PaypalOrder(models.Model):
    ''' cy_paypal_order '''
    _name = "cy.paypal.order"
    _log_access = False
    _sql_constraints = [('biz_order_on_unique', 'UNIQUE(biz_order_on)', 'biz_order_on不可重复')]

    biz_order_on = fields.Char(string='order_on(biz)', size=63)
