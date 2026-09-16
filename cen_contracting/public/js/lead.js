frappe.ui.form.on('Lead', {
    refresh: function(frm) {
        // Override standard make_opportunity to bypass the "Create Prospect" popup
        if (erpnext.LeadController) {
            erpnext.LeadController.prototype.make_opportunity = function() {
                frappe.model.open_mapped_doc({
                    method: "erpnext.crm.doctype.lead.lead.make_opportunity",
                    frm: this.frm,
                });
            };
        }
    }
});

