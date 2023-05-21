# -*- coding: utf-8 -*-
''' cy_base '''

import json
import hashlib
import random
import logging
from datetime import datetime
from dateutil import parser
import requests
import pytz
from odoo import fields, models, api

_logger = logging.getLogger(__name__)


class Base(models.AbstractModel):
    ''' cy_base '''
    _name = 'cy.base'
    _description = '公共组件'

    @api.model
    def convert_to_utc(self, data, tz='UTC-8', format_str=None):
        ''' local time str to utc str '''
        if data:
            timestamp = parser.parse('%s %s' % (data, tz))
            context_tz = pytz.timezone('UTC')
            if format_str:
                return timestamp.astimezone(context_tz).strftime(format_str)
            else:
                return fields.Datetime.to_string(timestamp.astimezone(context_tz))
        return None

    @api.model
    def convert_to_local(self, data, tz_name='Asia/Shanghai', format_str=None):
        ''' utc time str to local str '''
        if data:
            timestamp = parser.parse('%s UTC' % data)
            context_tz = pytz.timezone(tz_name)
            if format_str:
                return timestamp.astimezone(context_tz).strftime(format_str)
            else:
                return fields.Datetime.to_string(timestamp.astimezone(context_tz))
        return None

    @api.model
    def dbtime_since_seconds(self, data):
        ''' dbtime sub now '''
        d1 = datetime.strptime(data, '%Y-%m-%d %H:%M:%S')
        d2 = datetime.now()
        if d1 > d2:
            sub = d1 - d2
            seconds = sub.days * 24 * 3600 + sub.seconds
        else:
            sub = d2 - d1
            seconds = -(sub.days * 24 * 3600 + sub.seconds)
        return seconds

    @api.model
    def call_odoo(self, url, dbname, uid, password, object_name, method, param):
        datastr = json.dumps({
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute",
                "args": [dbname, uid, password, object_name, method, param]
            },
            "id": random.randint(0, 10000000)
        })
        return requests.post(url, data=datastr, headers={'content-type': 'application/json'}).json()

    @api.model
    def request_has_sign(self, server, data):
        try:
            if not data:
                data = {}
            time_src = datetime.now(pytz.utc)
            data['timestamp'] = time_src.strftime("%Y%m%d%H%M%S")
            data['nonceStr'] = '123456'
            strs = []
            for key in data.keys():
                strs.append("%s=%s" % (key, data[key]))
            strs.sort(reverse=False)
            sign = '%s&key=chuanmoon_SIGN_KEY' % ('&'.join(strs),)
            m = hashlib.md5()
            m.update(sign.encode('utf-8'))
            sign = (m.hexdigest()).upper()
            data['sign'] = sign
            return requests.post(server, data).json()
        except Exception as e:
            _logger.error(str(e))
        return ''

    @api.model
    def money_to_usd(self, amount, currency, rate):
        if currency == "JPY":
            return amount/rate
        # 临时方案
        return amount/100/rate

    @api.model
    def money_int_to_float(self, amount, currency):
        if currency == "JPY":
            return amount
        # 临时方案
        return amount/100


class MailThread(models.AbstractModel):
    ''' cy_mail_thread '''
    _name = 'cy.mail.thread'
    _inherit = 'mail.thread'
    _description = 'mail.thread公共组件'

    @api.model
    def fields_get(self, fields=None):
        hide = ['message_needaction',
                'message_follower_ids',
                'message_channel_ids',
                'message_partner_ids',
                'message_is_follower',
                'message_main_attachment_id',
                'message_has_error',
                ]
        res = super(MailThread, self).fields_get()
        for field in hide:
            res[field]['selectable'] = False
        return res
