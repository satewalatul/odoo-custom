# -*- coding: utf-8 -*-
# from odoo import http


# class CustomerBranch(http.Controller):
#     @http.route('/customer_branch/customer_branch', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/customer_branch/customer_branch/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('customer_branch.listing', {
#             'root': '/customer_branch/customer_branch',
#             'objects': http.request.env['customer_branch.customer_branch'].search([]),
#         })

#     @http.route('/customer_branch/customer_branch/objects/<model("customer_branch.customer_branch"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('customer_branch.object', {
#             'object': obj
#         })
