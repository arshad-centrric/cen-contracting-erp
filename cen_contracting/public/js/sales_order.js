frappe.ui.form.on('Sales Order', {
    setup: function(frm) {
        // Delivery Date is optional (see overrides/sales_order/optional_delivery_date.py), so stop
        // ERPNext's toggle_delivery_date from marking the item column mandatory on Sales orders
        frm.cscript.toggle_delivery_date = function() {
            frm.fields_dict.items.grid.toggle_reqd('delivery_date', false);
        };
    },
    onload: function(frm) {
        // If an existing project was mapped from Quotation but standard project field is empty
        if (frm.doc.cen_project_type === 'Existing' && frm.doc.cen_choose_project && !frm.doc.project) {
            frm.set_value('project', frm.doc.cen_choose_project);
        }
    },
    cen_choose_project: function(frm) {
        if (frm.doc.cen_project_type === 'Existing') {
            frm.set_value('project', frm.doc.cen_choose_project);
        }
    },
    cen_project_type: function(frm) {
        if (frm.doc.cen_project_type === 'Existing') {
            frm.set_value('project', frm.doc.cen_choose_project);
        } else {
            frm.set_value('project', '');
        }
    }
});

