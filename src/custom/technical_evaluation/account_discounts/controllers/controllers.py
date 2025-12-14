# -*- coding: utf-8 -*-
# from odoo import http


# class AccountDiscounts(http.Controller):
#     @http.route('/account_discounts/account_discounts', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_discounts/account_discounts/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_discounts.listing', {
#             'root': '/account_discounts/account_discounts',
#             'objects': http.request.env['account_discounts.account_discounts'].search([]),
#         })

#     @http.route('/account_discounts/account_discounts/objects/<model("account_discounts.account_discounts"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_discounts.object', {
#             'object': obj
#         })

