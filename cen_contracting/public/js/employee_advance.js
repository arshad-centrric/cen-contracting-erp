frappe.provide("cen_contracting");

frappe.ui.form.on("Employee Advance", {
    company: function(frm) {
        cen_contracting.apply_advance_type_mapping(frm);
    },
    cen_advance_type: function(frm) {
        cen_contracting.apply_advance_type_mapping(frm);
    },
    cen_loan_start_date: function(frm) {
        cen_contracting.compute_loan_end_date(frm);
    },
    cen_loan_term_months: function(frm) {
        cen_contracting.compute_loan_end_date(frm);
        cen_contracting.recompute_monthly_deduction(frm);
    },
    advance_amount: function(frm) {
        cen_contracting.recompute_monthly_deduction(frm);
    }
});

cen_contracting.apply_advance_type_mapping = function(frm) {
    if (!frm.doc.cen_advance_type || !frm.doc.company) {
        return;
    }

    frm.set_value("repay_unclaimed_amount_from_salary", frm.doc.cen_advance_type === "Petty Cash/Expense" ? 0 : 1);

    if (frm.doc.cen_advance_type === "Loan Advance" && !frm.doc.cen_loan_start_date) {
        frm.set_value("cen_loan_start_date", moment().add(1, "months").startOf("month").format("YYYY-MM-DD"));
    }

    frappe.call({
        method: "cen_contracting.cen_contracting.doctype.employee_advance_settings.employee_advance_settings.get_advance_type_mapping",
        args: {
            company: frm.doc.company,
            advance_type: frm.doc.cen_advance_type
        },
        callback: function(r) {
            if (r.message && r.message.advance_account) {
                frm.set_value("advance_account", r.message.advance_account);
            } else {
                frm.set_value("advance_account", "");
                frappe.msgprint({
                    title: __("Missing Mapping"),
                    indicator: "orange",
                    message: __(
                        "No Advance Account mapping found for Company {0} and Advance Type {1}. Configure it in Employee Advance Settings before saving.",
                        [frm.doc.company, frm.doc.cen_advance_type]
                    )
                });
            }
        }
    });
};

cen_contracting.compute_loan_end_date = function(frm) {
    if (frm.doc.cen_loan_start_date && frm.doc.cen_loan_term_months) {
        frm.set_value(
            "cen_loan_end_date",
            frappe.datetime.add_months(frm.doc.cen_loan_start_date, frm.doc.cen_loan_term_months)
        );
    }
};

cen_contracting.recompute_monthly_deduction = function(frm) {
    if (frm.doc.cen_advance_type === "Loan Advance" && frm.doc.cen_loan_term_months) {
        frm.set_value(
            "cen_monthly_deduction",
            flt(flt(frm.doc.advance_amount) / frm.doc.cen_loan_term_months, 2)
        );
    }
};
