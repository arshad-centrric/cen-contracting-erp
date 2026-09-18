frappe.ui.form.on('Quotation', {
    refresh: function(frm) {
        // Hide version number on unsaved drafts
        frm.toggle_display('cen_version_number', !frm.is_new());
        
        // Only show for cancelled documents
        if (frm.doc.docstatus === 2) {
            frm.page.set_primary_action(__('Revise Quotation'), function() {
                let d = new frappe.ui.Dialog({
                    title: __('Reason for Revision'),
                    fields: [
                        {
                            label: __('Reason'),
                            fieldname: 'reason',
                            fieldtype: 'Small Text',
                            reqd: 1
                        }
                    ],
                    primary_action_label: __('Revise'),
                    primary_action(values) {
                        d.hide();
                        
                        // Replicate standard amend_doc but inject the reason
                        frappe.xcall("frappe.client.is_document_amended", {
                            doctype: frm.doc.doctype,
                            docname: frm.doc.name,
                        }).then((is_amended) => {
                            if (is_amended) {
                                frappe.throw(__("This document is already amended, you cannot amend it again"));
                            }
                            
                            frm.validate_form_action("Amend");
                            let fn = function(newdoc) {
                                newdoc.amended_from = frm.docname;
                                newdoc.cen_revision_reason = values.reason; // Inject reason
                                if (frm.fields_dict && frm.fields_dict["amendment_date"]) {
                                    newdoc.amendment_date = frappe.datetime.obj_to_str(new Date());
                                }
                            };
                            
                            frm.copy_doc(fn, 1);
                            frappe.utils.play_sound("click");
                        });
                    }
                });
                d.show();
            });
        }
    }
});
