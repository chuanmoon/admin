# -*- coding: utf-8 -*-
from odoo import tools
from odoo import http
import time
from datetime import datetime
import random
import json
import base64
from hashlib import sha1 as sha
import hmac
from odoo.http import request
import requests
import json


class ProductController(http.Controller):
    @http.route('/cy_product/save_select_color_image', auth='user', csrf=False)
    def save_hotspots(self, req, **kw):
        skc_id = kw.get('skc_id', '')
        image = kw.get('image', '')

        if not skc_id:
            return '{"msg":"skc_id错误"}'
        if not image:
            return '{"msg":"image错误"}'

        skc_id = int(skc_id)
        if not skc_id:
            return '{"msg":"skc_id错误"}'

        sql = ''' update cy_product_skc
        set select_color_img=%(select_color_img)s, write_date=(now() AT TIME ZONE '0')
        where id=%(skc_id)s '''
        request.env.cr.execute(sql, {'select_color_img': image, 'skc_id': skc_id})

        return '{"msg":"保存成功"}'
