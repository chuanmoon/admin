from odoo import models, fields, api


class PayChannel(models.Model):
    ''' cy_payment_channel '''
    _name = "cy.payment.channel"
    _inherit = 'cy.mail.thread'

    code = fields.Char(string="渠道代码", size=31)
    config = fields.Text(string="JSON Config", tracking=True)
