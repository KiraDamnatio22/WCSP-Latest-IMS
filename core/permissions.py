from gui.admin_features.inventory import InventoryAdmin
from gui.admin_features.account import AccountAdmin
# from gui.admin_features.requests import RequestsAdmin
from gui.admin_features.manage_user import UserManagement
from gui.admin_features.request_feature import RequestItems
 

admin_access_list = {
    'Home': 'Full',
    'Inventory': InventoryAdmin,
    'Requests': RequestItems,
    # 'Request': '(Request Item, Approve Requests)',
    'Purchase Orders': 'Create/Track',
    'Suppliers': 'Manage',
    'Reports': 'Generate',
    'Manage User': UserManagement,
    'Settings': 'Full',
    'Help': '---',
    'Account': AccountAdmin,
}









# from gui.manager_dashboard import *
# from gui.technician_dashboard import *

# manager_access_list = {
#     'Home': 'Full',
#     'Inventory': 'Inventory (View, Stock Logs, Optional Override)',
#     'Request': '(Approve Requests)',
#     'Purchase Orders': 'Approve PO',
#     'Suppliers': 'View/Edit',
#     'Reports': 'Full',
#     'User Management': 'Full',
#     'Settings': 'Full',
#     'Help': '---'
# }

# technician_access_list = {
#     'Home': 'View Summary',
#     'Inventory': 'Inventory (View)',
#     'Request': '(Request Item)',
#     'Purchase Orders': 'NONE',
#     'Suppliers': 'NONE',
#     'Reports': 'NONE',
#     'User Management': 'NONE',
#     'Settings': 'NONE',
#     'Help': '---'
# }