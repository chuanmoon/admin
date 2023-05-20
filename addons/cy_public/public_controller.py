# -*- coding: utf-8 -*-
import logging
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
import qiniu

_logger = logging.getLogger(__name__)


class PublicController(http.Controller):
    @http.route('/uptoken', auth='public')
    def uptoken(self):
        ''' 上传token '''

        access_key = tools.config.get('qiniu_access_key', '')
        secret_key = tools.config.get('qiniu_secret_key', '')
        bucket = tools.config.get('bucket', '')
        qiniu_auth = qiniu.Auth(access_key, secret_key)
        return json.dumps({'uptoken': qiniu_auth.upload_token(bucket)})

    def do_save_imageinfo(self, name, old_name):
        url = 'https://img.your_domin.com/'+name + '-info'
        try:
            res = requests.get(url, timeout=5)
            if res.status_code != 200:
                return False

            image_info = json.loads(res.text)

            width = image_info.get('width')
            height = image_info.get('height')

            new_info = request.env['cy.image.info'].sudo().create({'url': name, 'image_w': width, 'image_h': height})

            hostspot_obj = request.env['cy.hotspot'].sudo()
            old_hotspots = hostspot_obj.search([('image_id.url', '=', old_name)])
            for old_hotspot in old_hotspots:
                hostspot_obj.create({
                    'action_id': old_hotspot.action_id.id,
                    'image_id': new_info.id,
                    'x': old_hotspot.x,
                    'y': old_hotspot.y,
                    'w': old_hotspot.w,
                    'h': old_hotspot.h,
                })
        except requests.exceptions.ConnectionError:
            return False
        except requests.exceptions.Timeout:
            return False

    @http.route('/public/imageinfo', auth='user')
    def save_imageinfo(self, req, **kw):
        name = kw.get('v', False)
        old_name = kw.get('ov', False)

        self.do_save_imageinfo(name, old_name)

    @http.route('/public/load_hotspots', auth='user', csrf=False)
    def load_hotspots(self, req, **kw):
        name = kw.get('v', False)
        if not name:
            return '[]'
        hostspot_obj = request.env['cy.hotspot'].sudo()
        hotspots = hostspot_obj.search([('image_id.url', '=', name)])
        result = []
        for hotspot in hotspots:
            result.append({
                'id': hotspot.id,
                'name': hotspot.name or '',
                'action_id': hotspot.action_id.id,
                'x': hotspot.x,
                'y': hotspot.y,
                'w': hotspot.w,
                'h': hotspot.h,
            })
        return json.dumps(result)

    @http.route('/public/save_hotspots', auth='user', csrf=False)
    def save_hotspots(self, req, **kw):
        datas = json.loads(kw.get('datas', '{}'))
        image_url = datas.get('url', '')
        items = datas.get('items', [])

        image_info = request.env['cy.image.info'].sudo().search([('url', '=', image_url)])
        if not image_info:
            self.do_save_imageinfo(image_url, '')
            image_info = request.env['cy.image.info'].sudo().search([('url', '=', image_url)])
        hostspot_obj = request.env['cy.hotspot'].sudo()

        add_items = []
        ids = []
        for item in items:
            item['image_id'] = image_info.id
            id = item.get('id', 0)
            if id:
                ids.append(id)
                record = hostspot_obj.browse(id)
                record.write(item)
            else:
                add_items.append(item)
        hostspot_obj.search([('image_id.id', '=', image_info.id), ('id', 'not in', tuple(ids))]).unlink()
        for item in add_items:
            hostspot_obj.create(item)

        return '{"msg":"保存成功"}'

    @http.route('/public/load_actions_by_ids', auth='user', csrf=False)
    def load_actions_by_ids(self, req, **kw):
        action_ids = json.loads(kw.get('action_ids', '[]'))
        if not action_ids:
            return '{}'
        result = {}
        actions = request.env['cy.action'].sudo().search([('id', 'in', tuple(action_ids))])
        for action in actions:
            result[str(action.id)] = action.name
        return json.dumps(result)

    @http.route('/public/load_actions_by_name', auth='user', csrf=False)
    def load_actions_by_name(self, req, **kw):
        name = kw.get('name', '')
        action_obj = request.env['cy.action'].sudo()

        result = []
        if not name:
            actions = action_obj.search([], limit=50)
        else:
            actions = action_obj.search([('name', 'ilike', name)], limit=50)
        for action in actions:
            result.append({
                'id': action.id,
                'name': action.name,
                'action_type': action.action_type,
                'target_data': action.target_data or '',
            })
        return json.dumps(result)

    @http.route('/public/categories', auth='user', csrf=False)
    def categories(self, req, **kw):
        category = request.env['cy.product.category'].sudo()
        result = []
        categories = category.search([('active', '=', True)])
        for cat in categories:
            parent = 0
            if cat.parent_id:
                parent = cat.parent_id.id

            info = [parent, cat.id, cat.name]
            result.append(info)
        return json.dumps(result)

    @http.route('/public/colors-sizes', auth='user', csrf=False)
    def colors_and_sizes(self, req, **kw):
        colordb = request.env['cy.product.color'].sudo()
        colors = colordb.search([], order='id')
        sizedb = request.env['cy.product.size'].sudo()
        sizes = sizedb.search([('active', '=', True)], order='id')

        result = []
        for color in colors:
            parent = 0
            if color.parent_id:
                parent = color.parent_id

            info = [parent, color.id, '%s-%s' % (color.name, color.display_name)]
            result.append(info)

        sizeList = []
        for item in sizes:
            sizeList.append({
                'id': item.id,
                'name': item.value
            })

        data = {
            'colors': result,
            'sizes': sizeList
        }
        return json.dumps(data)

    @http.route('/public/condition-skcs', auth='user', csrf=False)
    def condition_skc(self, req, **kw):
        body = {
            'conditionId': int(kw.get('conditionId', 0)),
            'page': int(kw.get('page', 1)),
            'size': 100
        }
        _logger.info(body)
        inside_gateway_link = tools.config.get('inside_gateway_link', 'http://172.17.0.1:9000/gateway')
        x = requests.post(inside_gateway_link+'/r/m/product_2.0_ProductApi.ConditionSkcs', json=body)
        return x.text
