# -*- coding: utf-8 -*-
# from odoo import http


# class StockAlerts(http.Controller):
#     @http.route('/stock_alerts/stock_alerts', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_alerts/stock_alerts/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_alerts.listing', {
#             'root': '/stock_alerts/stock_alerts',
#             'objects': http.request.env['stock_alerts.stock_alerts'].search([]),
#         })

#     @http.route('/stock_alerts/stock_alerts/objects/<model("stock_alerts.stock_alerts"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_alerts.object', {
#             'object': obj
#         })

