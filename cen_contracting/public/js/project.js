frappe.ui.form.on('Project', {
    onload: function(frm) {
        // Only run on new unsaved projects that are linked to a Sales Order
        if (frm.is_new() && frm.doc.sales_order) {
            // Fetch the custom project fields from the linked Sales Order
            frappe.db.get_value('Sales Order', frm.doc.sales_order, ['cen_project_type', 'cen_project_name'], (r) => {
                if (r && r.cen_project_type === 'New' && r.cen_project_name) {
                    frm.set_value('project_name', r.cen_project_name);
                }
            });
        }
    }
});

