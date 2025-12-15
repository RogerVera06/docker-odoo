from odoo import fields
from odoo.tests import TransactionCase

class TestAccountMoveDiscount(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        #Modelos
        cls.discount = cls.env['account.discount']
        cls.partner = cls.env['res.partner']
        cls.product = cls.env['product.product']
        cls.account_move = cls.env['account.move']
        cls.account_account = cls.env['account.account']

        #Descuento por tipo de cliente
        cls.discount_vip = cls.discount.create({'customer_type': 'VIP','percentage': 15.0,})

        #Cliente
        cls.customer_vip = cls.partner.create({'name': 'Cliente VIP','customer_type_id': cls.discount_vip.id,})

        # Crear cliente SIN política
        cls.customer_normal = cls.partner.create({'name': 'Cliente Sin Descuento','customer_type_id': False,})

        # Producto
        cls.product = cls.product.create({'name': 'Producto Test','list_price': 100.0,})

    def test_discount_applied_on_customer(self):
        #Flujo de publicacion de la factura
        move = self.account_move.create({
            'move_type': 'out_invoice',
            'partner_id': self.customer_vip.id,
            'invoice_line_ids': [
                (0, 0, {
                    'product_id': self.product.id,
                    'quantity': 1,
                    'price_unit': self.product.list_price,
                })
            ]
        })
        
        #Antes de publicar
        self.assertEqual(move.invoice_line_ids[0].discount, 0.0)

        move.action_post()

        # Despues de publicar
        self.assertEqual(move.invoice_line_ids[0].discount, 15.0)

    def test_no_discount_no_out_invoice(self):
        #Facturas que NO son "out_invoice"
        move = self.account_move.create({
            'move_type': 'in_invoice',
            'partner_id': self.customer_vip.id,
            #En caso de los 'in_invoice' es necesario asignarle una fecha
            'invoice_date': fields.Datetime.now(),
            'invoice_line_ids': [
                (0, 0, {
                    'product_id': self.product.id,
                    'quantity': 1,
                    'price_unit': self.product.list_price,
                })
            ]
        })
        
        move.action_post()
        
        # Despues de publicar
        self.assertEqual(move.invoice_line_ids[0].discount, 0.0)

    def test_no_discount_no_customer_type(self):
        #Facturas con clientes sin customer_type_id
        move = self.account_move.create({
            'move_type': 'out_invoice',
            'partner_id': self.customer_normal.id,
            'invoice_line_ids': [
                (0, 0, {
                    'product_id': self.product.id,
                    'quantity': 1,
                    'price_unit': self.product.list_price,
                })
            ]
        })
        
        move.action_post()
        
        # Despues de publicar
        self.assertEqual(move.invoice_line_ids[0].discount, 0.0)

    def test_multiple_lines_get_discount(self):
        #Multiples productos, todos deben recibir el mismo descuento
        move = self.account_move.create({
            'move_type': 'out_invoice',
            'partner_id': self.customer_vip.id,
            'invoice_line_ids': [
                (0, 0, {
                    'product_id': self.product.id,
                    'quantity': 2,
                    'price_unit': self.product.list_price,
                }),
                (0, 0, {
                    'product_id': self.product.id,
                    'quantity': 1,
                    'price_unit': self.product.list_price,
                })
            ]
        })
        move.action_post()
        
        # Despues de publicar
        for line in move.invoice_line_ids:
            self.assertEqual(line.discount, 15.0)