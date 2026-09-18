frappe.provide("cen_contracting");

frappe.ui.form.on("Expense Claim Detail", {
    cen_base_amount: function(frm, cdt, cdn) {
        cen_contracting.update_expense_total(frm, cdt, cdn);
    },
    cen_vat_amount: function(frm, cdt, cdn) {
        cen_contracting.update_expense_total(frm, cdt, cdn);
    }
});

cen_contracting.update_expense_total = function(frm, cdt, cdn) {
    let row = frappe.get_doc(cdt, cdn);
    let base = flt(row.cen_base_amount);
    let vat = flt(row.cen_vat_amount);
    
    if (base > 0 || vat > 0) {
        frappe.model.set_value(cdt, cdn, "amount", base + vat);
    }
};

frappe.ui.form.on("Expense Claim", {
    validate: function(frm) {
        let has_vat = false;
        
        $.each(frm.doc.expenses || [], function(i, row) {
            if (flt(row.cen_vat_amount) > 0) {
                has_vat = true;
                if (!row.cen_vendor_name) {
                    frappe.throw(`Row ${row.idx}: Vendor Name is mandatory when VAT is entered.`);
                }
                if (!row.cen_vendor_vat_number) {
                    frappe.throw(`Row ${row.idx}: Vendor VAT Number is mandatory when VAT is entered.`);
                }
            }
            
            let expense_type = (row.expense_type || "").toLowerCase();
            if (expense_type.includes("transportation") || expense_type.includes("fuel")) {
                if (!row.cen_vehicle_details) {
                    frappe.throw(`Row ${row.idx}: Vehicle Details are mandatory for Transportation and Fuel expenses.`);
                }
            }
        });
        
        if (has_vat && !frm.doc.cen_vat_account) {
            frappe.throw("VAT Account must be selected in the main form because one or more expenses include VAT.");
        }
    }
});
