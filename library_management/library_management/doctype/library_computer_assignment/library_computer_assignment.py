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

        # Check if there are available computers for assignment
        available_computers = frappe.get_all(
            'Library Computer',
            filters={
                'assignment_status': 'Available',
            },
            fields=['name']
        )

        if not available_computers:
            frappe.throw(_('The selected Computer is already assigned to another Member.'))

        # Ensure that each member is assigned only one computer
        assigned_computer = frappe.get_all(
            'Library Computer Assignment',
            filters={
                'library_member': self.library_member,
                'docstatus': 1,
            },
            fields=['name']
        )

        if assigned_computer:
            frappe.throw(_('This member is already assigned a computer. Only one assignment per member is allowed.'))

        # Assign the computer
        assigned_computer = available_computers[0]
        assigned_computer_doc = frappe.get_doc('Library Computer', assigned_computer.name)

        if assigned_computer_doc.assignment_status != 'Available':
            frappe.throw(_('The selected computer is already assigned.'))

        assigned_computer_doc.assignment_status = 'Assigned'
        assigned_computer_doc.library_member = self.library_member  # Link the computer to the library member
        assigned_computer_doc.save()
