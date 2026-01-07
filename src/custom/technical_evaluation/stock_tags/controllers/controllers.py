# -*- coding: utf-8 -*-
# from odoo import http


# class StockTags(http.Controller):
#     @http.route('/stock_tags/stock_tags', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_tags/stock_tags/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_tags.listing', {
#             'root': '/stock_tags/stock_tags',
#             'objects': http.request.env['stock_tags.stock_tags'].search([]),
#         })

#     @http.route('/stock_tags/stock_tags/objects/<model("stock_tags.stock_tags"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_tags.object', {
#             'object': obj
#         })

