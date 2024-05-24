from odoo import fields, models
from datetime import timedelta


class Property(models.Model):
    _name = "estate.property"
    _description = "Property"
    
    name = fields.Char(string='Property Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available From', copy=False, default=fields.Date.today() + timedelta(days=90))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('# of Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('# of Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(string='Garden Orientation', selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    active = fields.Boolean(default=True)
    state = fields.Selection(selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
                             copy=False, default='new', required=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesman_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False) 
    property_tag_ids = fields.Many2many("estate.property.tag", string="Property Tag")
    property_offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    
    