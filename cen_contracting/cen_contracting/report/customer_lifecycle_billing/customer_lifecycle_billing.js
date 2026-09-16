frappe.query_reports["Customer Lifecycle Billing"] = {
	"filters": [
		{
			"fieldname": "customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"fieldname": "quotation",
			"label": __("Quotation"),
			"fieldtype": "Link",
			"options": "Quotation",
			"get_query": function () {
				var customer = frappe.query_report.get_filter_value('customer');
				if (customer) {
					return { filters: { 'party_name': customer } };
				}
			}
		},
		{
			"fieldname": "sales_order",
			"label": __("Sales Order"),
			"fieldtype": "Link",
			"options": "Sales Order",
			"get_query": function () {
				var customer = frappe.query_report.get_filter_value('customer');
				if (customer) {
					return { filters: { 'customer': customer } };
				}
			}
		},
		{
			"fieldname": "invoice",
			"label": __("Sales Invoice"),
			"fieldtype": "Link",
			"options": "Sales Invoice",
			"get_query": function () {
				var customer = frappe.query_report.get_filter_value('customer');
				if (customer) {
					return { filters: { 'customer': customer } };
				}
			}
		}
	],
	"add_total_row": true
};