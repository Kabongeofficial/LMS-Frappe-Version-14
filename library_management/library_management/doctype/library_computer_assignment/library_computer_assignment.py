# Copyright (c) 2023, Kabonge and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

from frappe import _
import frappe
from frappe.model.document import Document

class LibraryComputerAssignment(Document):
    def validate(self):
        # Check for valid library membership
        valid_membership = frappe.get_all(
            'Library Membership',
            filters={
                'library_member': self.library_member,
                'docstatus': 1,
                'from_date': ('<=', self.assignment_time),
                'to_date': ('>=', self.assignment_time),
            },
            fields=['name']
        )

        if not valid_membership:
            frappe.throw(_('The member does not have a valid library membership.'))

        # Ensure that each member is assigned only one computer
        assigned_computer = frappe.get_all(
            'Library Computer Assignment',
            filters={
                'library_member': self.library_member,
                'docstatus': 1,
            },
            fields=['name']
        )

        if assigned_computer and assigned_computer[0].name != self.name:
            frappe.throw(_('This member is already assigned a computer. Only one assignment per member is allowed.'))
