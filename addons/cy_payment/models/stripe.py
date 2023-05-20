from odoo import models, fields


class StripeCustomer(models.Model):
    ''' cy_stripe_customer '''
    _name = 'cy.stripe.customer'
    _sql_constraints = [("user_id_unique", 'UNIQUE(user_id)', "用户唯一")]
    _log_access = False

    user_id = fields.Integer(string='用户ID')
    stripe_customer_id = fields.Char(string='stripe用户ID')
