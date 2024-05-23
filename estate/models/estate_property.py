from odoo import fields, models


class Property(models.Model):
    _name = "estate.property"
    _description = "Property"
    
    name = fields.Char(string='Property Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available From')
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float('Selling Price')
    bedrooms = fields.Integer('# of Bedrooms')
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('# of Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(string='Garden Orientation', selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    
    
    