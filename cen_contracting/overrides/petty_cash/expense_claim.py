import frappe
from frappe import _
from hrms.hr.doctype.expense_claim.expense_claim import ExpenseClaim
from frappe.utils import flt

class CustomExpenseClaim(ExpenseClaim):
    def get_gl_entries(self):
        gl_entry = []
        self.validate_account_details()

        # payable entry
        if self.grand_total:
            gl_entry.append(
                self.get_gl_dict(
                    {
                        "account": self.payable_account,
                        "credit": self.base_grand_total,
                        "credit_in_account_currency": self.grand_total,
                        "credit_in_transaction_currency": self.grand_total,
                        "against": ",".join([d.default_account for d in self.expenses]),
                        "party_type": "Employee",
                        "party": self.employee,
                        "against_voucher_type": self.doctype,
                        "against_voucher": self.name,
                        "cost_center": self.cost_center,
                        "project": self.project,
                        "transaction_exchange_rate": self.exchange_rate,
                    },
                    account_currency=self.currency,
                    item=self,
                )
            )

        # expense entries
        for data in self.expenses:
            base_amount = flt(data.get("cen_base_amount") or 0)
            vat_amount = flt(data.get("cen_vat_amount") or 0)
            
            if not base_amount and not vat_amount:
                # Standard flow if custom fields are not used
                gl_entry.append(
                    self.get_gl_dict(
                        {
                            "account": data.default_account,
                            "debit": data.base_sanctioned_amount,
                            "debit_in_account_currency": data.sanctioned_amount,
                            "debit_in_transaction_currency": data.sanctioned_amount,
                            "against": self.employee,
                            "cost_center": data.cost_center or self.cost_center,
                            "project": data.project or self.project,
                            "transaction_exchange_rate": self.exchange_rate,
                        },
                        account_currency=self.currency,
                        item=data,
                    )
                )
            else:
                # Custom Flow: Split into Base and VAT
                # Base Amount goes to Expense Account
                if base_amount > 0:
                    sanctioned_base = base_amount # Assuming fully sanctioned for custom flow
                    if flt(data.sanctioned_amount) < flt(data.amount) and flt(data.amount) > 0:
                        # If partially sanctioned, prorate the base
                        sanctioned_base = base_amount * (flt(data.sanctioned_amount) / flt(data.amount))
                        
                    gl_entry.append(
                        self.get_gl_dict(
                            {
                                "account": data.default_account,
                                "debit": sanctioned_base * self.exchange_rate,
                                "debit_in_account_currency": sanctioned_base,
                                "debit_in_transaction_currency": sanctioned_base,
                                "against": self.employee,
                                "cost_center": data.cost_center or self.cost_center,
                                "project": data.project or self.project,
                                "transaction_exchange_rate": self.exchange_rate,
                            },
                            account_currency=self.currency,
                            item=data,
                        )
                    )
                
                # VAT Amount goes to VAT Account
                if vat_amount > 0:
                    sanctioned_vat = vat_amount
                    if flt(data.sanctioned_amount) < flt(data.amount) and flt(data.amount) > 0:
                        sanctioned_vat = vat_amount * (flt(data.sanctioned_amount) / flt(data.amount))
                        
                    vat_account = self.get("cen_vat_account")
                    if not vat_account:
                        frappe.throw(_("VAT Account must be specified on the Expense Claim when expenses include VAT."))
                        
                    gl_entry.append(
                        self.get_gl_dict(
                            {
                                "account": vat_account,
                                "debit": sanctioned_vat * self.exchange_rate,
                                "debit_in_account_currency": sanctioned_vat,
                                "debit_in_transaction_currency": sanctioned_vat,
                                "against": self.employee,
                                "cost_center": data.cost_center or self.cost_center,
                                "project": data.project or self.project,
                                "transaction_exchange_rate": self.exchange_rate,
                            },
                            account_currency=self.currency,
                            item=data,
                        )
                    )

        # gl entry against advance
        for data in self.advances:
            if data.allocated_amount:
                gl_entry.append(
                    self.get_gl_dict(
                        {
                            "account": data.advance_account,
                            "credit": data.allocated_amount * self.exchange_rate,
                            "credit_in_account_currency": data.allocated_amount,
                            "credit_in_transaction_currency": data.allocated_amount,
                            "against": ",".join([d.default_account for d in self.expenses]),
                            "party_type": "Employee",
                            "party": self.employee,
                            "against_voucher_type": "Employee Advance",
                            "against_voucher": data.employee_advance,
                            "cost_center": self.cost_center,
                            "project": self.project,
                            "transaction_exchange_rate": self.exchange_rate,
                        },
                        account_currency=self.currency,
                        item=data,
                    )
                )

        # tax entries (Standard ERPNext Tax table support)
        if hasattr(self, "taxes"):
            for tax in self.taxes:
                if flt(tax.tax_amount):
                    company_currency = frappe.get_cached_value("Company", self.company, "default_currency")
                    account_currency = frappe.db.get_value("Account", tax.account_head, "account_currency") or company_currency
                    gl_entry.append(
                        self.get_gl_dict(
                            {
                                "account": tax.account_head,
                                "debit": tax.base_tax_amount,
                                "debit_in_account_currency": tax.base_tax_amount if account_currency == company_currency else tax.tax_amount,
                                "debit_in_transaction_currency": tax.base_tax_amount if account_currency == company_currency else tax.tax_amount,
                                "against": self.employee,
                                "cost_center": tax.cost_center or self.cost_center,
                                "project": self.project,
                                "transaction_exchange_rate": self.exchange_rate,
                            },
                            account_currency=account_currency,
                            item=tax,
                        )
                    )
                    
        return gl_entry
