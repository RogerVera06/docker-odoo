from odoo import _, api, fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    min_stock_qty = fields.Integer(
        string="Minimum Stock Quantity",
        help="Inventory threshold that triggers stock alerts",
        default=0,
    )
    is_below_minimum = fields.Boolean(
        compute="_compute_is_below_minimum",
        store=True
    )

    last_stock_alert = fields.Date(
        string="Last Stock Alert Date",
    )

    @api.depends("qty_available", "min_stock_qty")
    def _compute_is_below_minimum(self):
        #Verifica si la cantidad del producto es menor al minimo establecido
        for record in self:
            record.is_below_minimum = True if record.qty_available < record.min_stock_qty else False
    
    def _send_alert(self):
        if self.is_below_minimum:
            root_partner = self.env.ref("base.partner_root")
            channel = self.env.ref("stock_alerts.channel_stock_critical_alerts")

            #Verifica si la ultima alerta fue el dia de hoy
            if self.last_stock_alert == fields.Date.today():
                return
            
            #Creamos el mensaje de alerta:
            message = _("The product '%s' is below the minimum stock quantity: %s. Current stock: %s.") % (self.name,self.min_stock_qty,self.qty_available)

            #Se publica el mensaje en el chatter del producto
            self.message_post(
                body=message,
                message_type="comment",
                subtype_xmlid="mail.mt_comment",
                author_id=root_partner.id,
            )

            #Y en el canal creado para las alertas de stock
            channel.message_post(
                body=message,
                message_type="comment",
                subtype_xmlid="mail.mt_comment",
                author_id=root_partner.id,
            )

            self.last_stock_alert = fields.Date.today()
            
    def _cron_send_stock_alerts(self):
        #Accion planificada para enviar alertas
        products = self.search([('is_below_minimum', '=', True)])
        for product in products:
            product._send_alert()