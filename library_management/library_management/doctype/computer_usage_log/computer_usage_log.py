# Copyright (c) 2023, Kabonge and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class ComputerUsageLog(Document):
	pass
def release_computer_on_change(doc, method):
    if doc.release_computer:
        # Find the linked Library Computer Assignment
        computer_assignment = frappe.get_doc("Library Computer Assignment", doc.computer_assignment)
        if computer_assignment:
            # Update the assignment status to 'Available'
            computer_assignment.db_set("assignment_status", "Available")