from odoo import models,fields,api


class ClientInfo(models.Model):
    _name = 'client.info'
    _inherits = {'res.partner': 'partner_id'}
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Relational Fields
    partner_id = fields.Many2one('res.partner',
                                 required=True,
                                 ondelete='restrict',
                                 auto_join=True, 
                                 index=True,
                              string='Related Partner')
    # _inherits = ['res.partner']
    active = fields.Boolean(string='Active',default=True)
    is_organization = fields.Boolean(string='Is Organization',default=True)

    client_name = fields.Char('Client',required=True)
    branch_ids = fields.One2many('branch.info','related_client_id', string='Branches',)
    client_location = fields.Char("Client Location", invisible=True)  # Set readonly to False initially
    client_additional_info = fields.Char('Notes')
    
    
    @api.model
    def create(self,vals):
        if vals['is_organization'] == True:
            vals['is_company'] = True
        vals['name'] = vals['client_name']
        return super(ClientInfo,self).create(vals)
       
                
    

class BranchInfo(models.Model):
    _name = 'branch.info'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Branch Name', required=True)
    related_client_id = fields.Many2one('client.info', string='Client', domain="[('is_organization', '=', True)]",required=True)
    location = fields.Char(string='Location',required=True)
    active = fields.Boolean(string="Active",default=True)
    additional_info = fields.Char(string='Notes')    

    