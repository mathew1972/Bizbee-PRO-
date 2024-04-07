# In your custom app's Python module (e.g., custom_app/custom_app/notifications.py)
import frappe

@frappe.whitelist()
def check_expiry_reminders():
    today = datetime.today()
    thirty_days_later = today + timedelta(days=30)
    
    reminders = frappe.get_all("Reminder", filters={"date_of_expiry": ("<", thirty_days_later)}, fields=["name"])
    
    if reminders:
        # Send notification to the user
        user = frappe.session.user
        message = "Some services are going to expire. Please check the Reminder."
        frappe.publish_realtime(event="show_notification", message=message, user=user)

# Trigger the function on login
def trigger_on_login():
    check_expiry_reminders()
