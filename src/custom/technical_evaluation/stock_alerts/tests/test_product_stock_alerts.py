from odoo.tests import TransactionCase
from odoo import fields

class TestProductStockAlert(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        #Producto de prueba
        cls.product = cls.env['product.template'].create({
            'name': 'Test Product',
            'type': 'product',
            'min_stock_qty': 6,
        })
        
        #Definimos el stock como 5 (Debajo del minimo)
        cls.product.qty_available = 5

        #Verificar la exisitencia del canal de alertas
        try:
            cls.channel = cls.env.ref('stock_alerts.channel_stock_critical_alerts')
        except ValueError:
            cls.channel = cls.env['discuss.channel'].create({
                'name': 'Stock Critical Alerts',
                'channel_type': 'channel',
            })

    def test_send_alert_creates_messages_in_product_and_channel(self):
        #Verifica que debe enviar la alerta al chatter y al canal de alertas
        self.product._send_alert()
        
        #Debe registrar la fecha de hoy
        self.assertEqual(self.product.last_stock_alert, fields.Date.today())
        
        #Verifica la alerta en el chatter del producto
        product_messages = self.env['mail.message'].search([
            ('model', '=', 'product.template'),
            ('res_id', '=', self.product.id),
            ('body', 'ilike', 'Test Product'),
        ])
        self.assertEqual(len(product_messages), 1)
        self.assertIn("minimum stock quantity: 6", product_messages[0].body)
        
        #Verifica la alerta en el canal de alertas
        channel_messages = self.env['mail.message'].search([
            ('model', '=', 'discuss.channel'),
            ('res_id', '=', self.channel.id),
            ('body', 'ilike', 'Test Product'),
        ])
        self.assertEqual(len(channel_messages), 1)

    def test_no_alert_sent_if_stock_is_sufficient(self):
        #No hay alerta si esta por encima del minimo
        #Definimos el stock como 9 (Encima del minimo)
        self.product.qty_available = 9
        
        #is_below_minimum debe ser False
        self.assertFalse(self.product.is_below_minimum)
        
        #Se intenta enviar la alerta
        self.product._send_alert()
        
        #Debe ser falso
        self.assertFalse(self.product.last_stock_alert)
        
        #No debe haber mensajes
        messages = self.env['mail.message'].search([('body', 'ilike', 'Test Product')])
        self.assertEqual(len(messages), 0)

    def test_no_duplicate_alert_on_same_day(self):
        #Solo se permite una alerta por dia
        #Primera alerta
        self.product._send_alert()
        first_alert_date = self.product.last_stock_alert
        self.assertEqual(first_alert_date, fields.Date.today())
        
        #Contar mensajes antes de la segunda llamada
        first_message_count = self.env['mail.message'].search_count([
            ('body', 'ilike', 'Test Product')
        ])
        
        #Segunda llamada (mismo día)
        self.product._send_alert()
        
        #La fecha no debe cambiar
        self.assertEqual(self.product.last_stock_alert, first_alert_date)
        
        #El número de mensajes no debe aumentar
        final_message_count = self.env['mail.message'].search_count([
            ('body', 'ilike', 'Test Product')
        ])
        self.assertEqual(first_message_count, final_message_count)