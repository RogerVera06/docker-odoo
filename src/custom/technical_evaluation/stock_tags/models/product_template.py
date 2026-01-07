from odoo import _, api, fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    stock_storage_tag_ids = fields.Many2many(
        "stock.storage.tag",
        string="Smart Storage Tags",
        help="Allows the selection of 1 or more smart tags",)