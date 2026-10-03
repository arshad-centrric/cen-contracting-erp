class OptionalDeliveryDateMixin:
	def validate_delivery_date(self):
		# ERPNext throws "Please enter Delivery Date" on every Sales type order; only run its
		# checks (syncing item/parent dates, date not before the order) once a date is entered.
		if not self.delivery_date and not any(d.delivery_date for d in self.get("items")):
			return

		super().validate_delivery_date()
