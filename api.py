# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE
import base64
import binascii
import json
from urllib.parse import urlencode, urlparse

import frappe
import frappe.client
import frappe.handler
from frappe import _
from frappe.utils.data import sbool
from frappe.utils.password import get_decrypted_password
from frappe.utils.response import build_response
from frappe.model.document import Document


@frappe.whitelist()
def get_service_filter(custom_business_type):
    service = frappe.db.sql(f""" SELECT item_code, item_name, department, description FROM `tabCategory Service` WHERE category= '{custom_business_type}' """, as_dict=True)
    return service



                                      


