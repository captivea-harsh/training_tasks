from xmlrpc import client
from pandas import ExcelFile
import openpyxl


url = 'http://localhost:1618'
db = 'odoo16_april_28_db'
username = 'admin'
password = 'admin'
file_name_with_path ='/home/konsultoo-dhaval/workspace/odoo_16/odoo/custom_addons/Stock_location_script/Vision21 Bin Locations.xlsx'


common = client.ServerProxy('{}/xmlrpc/2/common'.format(url))
common.version()
uid = common.authenticate(db, username, password, {})
models = client.ServerProxy('{}/xmlrpc/2/object'.format(url))


xls = ExcelFile(file_name_with_path)
data = xls.parse(xls.sheet_names[0])
column_count = len(data)
data = data.to_dict()


count = 0
for i in range(0, column_count):
    count += 1

    Location_name = data.get('Parent Location').get(i)
    # print('Location_name............', Location_name)

    Parent_location = data.get('Warehouse').get(i)
    # print('Parent_location......', Parent_location)

    child_location = data.get('Location Name').get(i)
    # print('child_location......', child_location)



    # ------------------------------------- creating locations------------------------------------------------------------

    record_exist = models.execute_kw(db, uid, password, 'stock.location', 'search', [[('name', '=', Location_name), ('location_id', '=', Parent_location )]])
    # print(record_exist)

    vals_location = {
        'name': child_location,
        'location_id': record_exist[0]
    }
    # print('vals_location', vals_location)

    create_child_location = models.execute_kw(db, uid, password, 'stock.location', 'create', [vals_location])
    print('create_child_location', create_child_location)















