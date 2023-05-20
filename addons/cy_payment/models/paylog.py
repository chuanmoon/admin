from odoo import models, fields


class Paylog(models.Model):
    _name = "cy.payment.paylog"
    _order = "create_date desc"
    _sql_constraints = [("order_unique", 'UNIQUE(order_id,order_type)', "订单唯一")]

    _order_type_selections = [
        ("1", "普通订单")
    ]
    _fund_type_selections = [
        ("1", "入账"),
        ("2", "出账"),
        ("3", "-")
    ]

    union_id = fields.Char(string="全局Id", required=True, index=True, readonly=True, size=63)
    third_platform_reference_id = fields.Char(string='第三方支付平台ID', readonly=True, size=63)
    order_id = fields.Char(string="订单ID", readonly=True, size=63)
    order_type = fields.Selection(string="订单类型", selection=_order_type_selections, readonly=True, size=31)
    channel_id = fields.Many2one('cy.payment.channel', string="支付渠道", readonly=True)
    fund_type = fields.Selection(string="交易类型", selection=_fund_type_selections, size=31)
    amount = fields.Float(string="金额(USD)", readonly=True)
    currency = fields.Char(string='币种', readonly=True, size=15)
    desc = fields.Char(string="", readonly=True, size=127)


class PayOrder(models.Model):
    _name = 'cy.payment.payorder'
    _order = "create_date desc"
    _inherit = "cy.mail.thread"
    _sql_constraints = [("biz_order_unique", 'UNIQUE(biz_order_no)', "订单唯一"), ('pay_order_no_unique', 'UNIQUE(pay_order_no)', '支付单号唯一')]

    biz_order_no = fields.Char(string="业务订单ID", readonly=True, size=63)
    pay_order_no = fields.Char(string='支付流水号', readonly=True, size=63)
    transaction_ids = fields.Char(string='交易流水号', size=1024, readonly=True)
    pay_channel = fields.Char(string='支付渠道', index=True, size=31)
    amount = fields.Integer(string='支付金额(Int)')
    currency = fields.Char(string='支付币种', size=15)
    tax_type = fields.Char(string='支付者税号类型', size=15)
    tax_code = fields.Char(string='税号', size=31)

    from_platform = fields.Char(string="支付平台", size=31)

    pay_status = fields.Selection(string='支付状态', selection=[('1', '等待支付'), ('2', '等待收款'), ('3', '已完成'), ('4', '已取消')], tracking=True, size=31)

    receive_date = fields.Datetime(string='收款时间')
    cancel_date = fields.Datetime(string='取消时间')
    complete_date = fields.Datetime(string='完成时间')

    paypal_link = fields.Char(string='paypal 支付跳转连接', size=255)

    return_url = fields.Char(string='支付完成跳转链接', size=255)
    err_return_url = fields.Char(string='支付失败页面', size=255)
