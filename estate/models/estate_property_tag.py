from odoo import fields, models

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"
    _order = 'name'
    
    name = fields.Char("Name", required=True)
    color = fields.Integer()
    
    _sql_constraints = [
        ('check_unique_tag', 'UNIQUE(name)', 'The tag name has to be unique.'),
    ]