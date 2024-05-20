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

# your_module/api.py
@frappe.whitelist()
def get_purchase_update_data():
    purchase_update_data = frappe.get_all('Purchase Update', 
                                          filters={'status': 'PO Pending', 'department': ('!=', 'Self')}, 
                                          fields=['item_code','name','item_name', 'department', 'estimate_no', 'client_name'])
    return purchase_update_data



@frappe.whitelist()
def check_price(item_code):
    # Query to fetch the relevant data from the database
    price_data = frappe.db.sql("""
        SELECT
            ip.item_code,
            ip.item_name,
            ip.price_list_rate,
            ip.valid_from
        FROM
            `tabItem Price` ip
        WHERE
            ip.item_code = %s
            AND ip.price_list = 'Standard Selling'
        ORDER BY
            ip.valid_from DESC
        LIMIT 1
    """, (item_code), as_dict=True)

    if price_data:
        return price_data[0]
    else:
        frappe.throw(_("Price not found for this item."))


@frappe.whitelist()
def custom_update_rate(item_code):
    # Query to fetch the relevant data from the database
    price_data = frappe.db.sql("""
        SELECT
            ip.item_code,
            ip.item_name,
            ip.price_list_rate,
            ip.valid_from
        FROM
            `tabItem Price` ip
        WHERE
            ip.item_code = %s
            AND ip.price_list = 'Standard Selling'
        ORDER BY
            ip.valid_from DESC
        LIMIT 1
    """, (item_code), as_dict=True)

    if price_data:
        return price_data[0]
    else:
        frappe.throw(_("Price not found for this item."))


@frappe.whitelist()
def fetch_purchase_invoice_data():
    # Fetch data from Item Price doctype where conditions are met
    data = frappe.db.sql("""
        SELECT ip.item_code, ip.item_name, ip.price_list_rate, ip.valid_from
        FROM `tabItem Price` ip
        WHERE ip.price_list = 'Standard Buying'
        AND ip.valid_from = (SELECT MAX(valid_from) FROM `tabItem Price` WHERE item_code = ip.item_code AND price_list = 'Standard Buying')
        AND ip.item_code NOT IN (
            SELECT DISTINCT pi.item_code
            FROM `tabPurchase Invoice Item` pi
            WHERE pi.rate = (SELECT ip.price_list_rate FROM `tabItem Price` ip WHERE ip.item_code = pi.item_code AND ip.price_list = 'Standard Buying')
        )
    """, as_dict=True)

    return data

# Estimate Rate Slab
@frappe.whitelist()
def get_service_price_rule(item_code):
    print("Received Item Code:", item_code)  # Log the received item code

    # Fetch Service Price Rule based on item_code
    service_price_rule = frappe.get_all("Service Price Rule",
                                        filters={"service_code": item_code},
                                        fields=["name"])
    print("Service Price Rule:", service_price_rule)  # Log the fetched service price rule

    if service_price_rule:
        # Fetch Price Slabs for the Service Price Rule
        price_slabs = frappe.get_all("Price Slab",
                                      filters={"parent": service_price_rule[0].name},
                                      fields=["price_slab", "selling_rate", "markup_"])
        print("Price Slabs:", price_slabs)  # Log the fetched price slabs

        return {"price_slabs": price_slabs}
    else: 
        return None
