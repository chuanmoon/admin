from odoo import models, fields, api


class MailingList(models.Model):
    ''' cy_mailing_list '''
    _name = 'cy.mailing.list'
    _description = '邮件列表'
    _log_access = False
    _sql_constraints = [('email_unique', 'UNIQUE(email)', 'email不可重复')]
    _order = 'id desc'

    email = fields.Char(string='邮件', size=127)
    create_date = fields.Datetime(string='时间')
