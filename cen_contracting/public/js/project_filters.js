frappe.provide("cen_contracting");

cen_contracting.apply_project_filters = function(frm) {
    frm.set_query("cen_choose_project", function() {
        let party = frm.doc.customer || frm.doc.party_name || frm.doc.lead || "";
        
        return {
            filters: [
                ['Project', 'customer', 'in', [party, '']]
            ]
        };
    });
};

cen_contracting.clear_linked_fields = function(frm) {
    frm.set_value("cen_choose_project", "");
    
    if (frm.fields_dict.project) frm.set_value("project", "");
    if (frm.fields_dict.customer_address) frm.set_value("customer_address", "");
    if (frm.fields_dict.contact_person) frm.set_value("contact_person", "");
    if (frm.fields_dict.shipping_address_name) frm.set_value("shipping_address_name", "");
};

cen_contracting.sync_to_standard = function(frm) {
    if (frm.fields_dict.project && frm.doc.cen_choose_project && frm.doc.cen_choose_project !== frm.doc.project) {
        frm.set_value("project", frm.doc.cen_choose_project);
    }
};

cen_contracting.sync_from_standard = function(frm) {
    if (frm.fields_dict.project && frm.doc.project && frm.doc.project !== frm.doc.cen_choose_project) {
        frm.set_value("cen_choose_project", frm.doc.project);
    }
};

cen_contracting.fetch_party_details = function(frm) {
    if (frm.doc.party_name && frm.doc.opportunity_from) {
        let fields = frm.doc.opportunity_from === 'Lead' ? ['lead_name', 'company_name'] : ['customer_name'];
        frappe.db.get_value(frm.doc.opportunity_from, frm.doc.party_name, fields, function(r) {
            if (r && r.message) {
                frm.set_value('cen_party_name_details', r.message.lead_name || r.message.customer_name || '-');
                frm.set_value('cen_party_organization', r.message.company_name || '-');
            }
            frm.__fetching_party = false;
        });
    } else {
        frm.set_value('cen_party_name_details', '');
        frm.set_value('cen_party_organization', '');
        frm.__fetching_party = false;
    }
};

// Bind to Opportunity
frappe.ui.form.on("Opportunity", {
    setup: function(frm) {
        cen_contracting.apply_project_filters(frm);
    },
    refresh: function(frm) {
        frm.set_df_property("contact_person", "reqd", 1);
        frm.set_df_property("contact_mobile", "reqd", 1);
        cen_contracting.sync_from_standard(frm);
        
        if (!frm.doc.company) {
            let default_company = frappe.defaults.get_default("company") || frappe.defaults.get_user_default("Company");
            if (default_company) {
                frm.set_value("company", default_company);
            }
        }
        
        if (frm.doc.party_name && !frm.doc.cen_party_name_details && !frm.__fetching_party) {
            frm.__fetching_party = true;
            cen_contracting.fetch_party_details(frm);
        }
    },
    party_name: function(frm) {
        cen_contracting.clear_linked_fields(frm);
        cen_contracting.fetch_party_details(frm);
    },
    cen_choose_project: function(frm) {
        cen_contracting.sync_to_standard(frm);
    },
    project: function(frm) {
        cen_contracting.sync_from_standard(frm);
    }
});

// Bind to Quotation
frappe.ui.form.on("Quotation", {
    setup: function(frm) {
        cen_contracting.apply_project_filters(frm);
    },
    refresh: function(frm) {
        cen_contracting.sync_from_standard(frm);
    },
    customer: function(frm) {
        cen_contracting.clear_linked_fields(frm);
    },
    cen_choose_project: function(frm) {
        cen_contracting.sync_to_standard(frm);
    },
    project: function(frm) {
        cen_contracting.sync_from_standard(frm);
    }
});

// Bind to Sales Order
frappe.ui.form.on("Sales Order", {
    setup: function(frm) {
        cen_contracting.apply_project_filters(frm);
    },
    refresh: function(frm) {
        cen_contracting.sync_from_standard(frm);
    },
    customer: function(frm) {
        cen_contracting.clear_linked_fields(frm);
    },
    cen_choose_project: function(frm) {
        cen_contracting.sync_to_standard(frm);
    },
    project: function(frm) {
        cen_contracting.sync_from_standard(frm);
    }
});

