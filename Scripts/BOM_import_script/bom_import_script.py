from xmlrpc import client
from pandas import ExcelFile


url = 'http://localhost:1618'
db = 'odoo16_new_db_april_27_'
username = 'admin'
password = 'admin'
file_name_with_path ='/home/konsultoo-dhaval/workspace/odoo_16/odoo/custom_addons/BOM_script/bom_script_new.xlsx'


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

    product_name= data.get('ProductName').get(i)
    # print('product_name............', product_name)
    default_code_product= data.get('ProductSKU').get(i)
    # print('default_code_product.....',default_code_product )
    component_name= data.get('ComponentName').get(i)
    # print('component_name......', component_name)
    default_code_component= data.get('ComponentSKU').get(i)
    # print("internal_ref.......", default_code_component)
    component_qty= data.get('Quantity').get(i)
    # print('component_qty.....',component_qty )

    # -------------------------------------creating products------------------------------------------------------------

    product_id = models.execute_kw(db, uid, password, 'product.template', 'search', [[('default_code', '=', default_code_product)]])

    if not product_id:

        vals_product = {
            'default_code': default_code_product,
            'name': product_name
        }
        print('vals_product',vals_product )

        product_id = models.execute_kw(db, uid, password, 'product.template', 'create', [vals_product])
        print('create_product_template', product_id)

    else:
        product_id = product_id[0]

    print('product_id',product_id )

    #  ------------------------------------creating bom----------------------------------------------------------
    bom_id = models.execute_kw(db, uid, password, 'mrp.bom', 'search',[[('product_tmpl_id', '=', product_id)]])

    if not bom_id:

        vals_bom ={
            'product_tmpl_id' : product_id,
        }
        print('vals_productbom', vals_bom)

        bom_id = models.execute_kw(db, uid, password, 'mrp.bom', 'create', [vals_bom])
        print('bom_id', bom_id)

    else:

        bom_id = bom_id[0]

    print('bom_id', bom_id)

    #   ------------------------------creating components---------------------------------------------

    component_id = models.execute_kw(db, uid, password, 'product.product', 'search',[[('default_code', '=', default_code_component)]])

    if not component_id:

        vals_component = {
            'default_code': default_code_component,
            'name': component_name
        }
        print('vals_component', vals_component)

        component_id = models.execute_kw(db, uid, password, 'product.product', 'create', [vals_component])
        print('component_id', component_id)

    else:

        component_id = component_id[0]

    print('component_id', component_id)

    #   --------------------------- creating bom lines without searches------------------------------

    vals_bom_lines= {
                'bom_id' : bom_id,
                'product_id' : component_id,
                'product_qty' : component_qty
            }
    print('vals_bom_lines--------',vals_bom_lines )

    create_bom_lines = models.execute_kw(db, uid, password, 'mrp.bom.line', 'create', [vals_bom_lines])
    print('create_bom_lines--------', create_bom_lines)

