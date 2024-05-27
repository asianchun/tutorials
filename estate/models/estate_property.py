from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta


class Property(models.Model):
    _name = "estate.property"
    _description = "Property"
    _order = "id desc"
    
    # Creating fields
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
    
    # Reserved fields
    # If active is false, automatically disable it from any search
    active = fields.Boolean(default=True)
    state = fields.Selection(selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
                             copy=False, default='new', required=True)
    
    # Foreign Key fields
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesman_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False) 
    property_tag_ids = fields.Many2many("estate.property.tag", string="Property Tag")
    property_offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    
    # Calculated fields
    total_area = fields.Integer(compute="_compute_area")
    best_price = fields.Float(compute="_compute_best_price")
    
    # Add simple constraints
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be a positive number.'),
        ('check_selling_price', 'CHECK(selling_price > 0)', 'The selling price must be a positive number.'),
    ]
    
    # Defining menu button actions
    def action_set_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Cancelled properties cannot be sold.")
            
            record.state  = 'sold'
        
        return True
    
    def action_set_cancelled(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot be cancelled.")
            
            record.state = 'cancelled'
        
        return True
    
    # Define computed fields
    @api.depends("living_area", 'garden_area')
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    @api.depends("property_offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.property_offer_ids:
                record.best_price = max(record.property_offer_ids.mapped('price'))
            else:
                record.best_price = 0.0
    
    # Perform on change actions        
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''
    
    # Add complicated constraints
    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price <= record.expected_price * 0.9:
                raise ValidationError("The selling price cannot be less than 90% of the expected price! You must reduce the expected price if you want to accept the offer")
    