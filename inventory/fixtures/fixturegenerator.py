# %%
import json
import csv
import pandas as pd
# %%

#Generate product unit size fixtures
ml = [3, 3.5, 15, 25, 30, 50, 60, 100, 110, 150]
gm = [20, 25, 30, 75]
pc = [1]
units = [pc, gm, ml]
suffixes = ['pc', 'gm', 'ml']
unit_size = []
pk = 1

for index, unit in enumerate(units):
    for value in unit:
        suffix = suffixes[index]
        rec = {
            "model": "inventory.ProductUnitSize",
            "pk": pk,
            "fields": {
                "value": value,
                "unit": str(suffix),
                "sku_part": str(value)+str(suffix.upper())
            }
        }
        unit_size.append(rec)
        pk += 1

with open('./productunitsize.json', 'w') as json_file:
    json.dump(unit_size, json_file)


# %%
#Generate product fixtures
excel_file_path = "../management/data/Product.xlsx"

df = pd.read_excel(excel_file_path)

# Convert the DataFrame to a JSON string
json_string = df.to_json(orient='records', indent=4)

#Link foreign keys
new_json_data = []
product = json.loads(json_string)
with open('inventorycategory.json', 'r') as data1:
    inventorycat = json.load(data1) 
with open('productbrand.json', 'r') as data2:
    brand = json.load(data2) 
with open('productpackagesize.json', 'r') as data3:
    pkgsize = json.load(data3) 
with open('productunitsize.json', 'r') as data4:
    unitsize = json.load(data4)
with open('productvariant.json', 'r') as data5:
    variant = json.load(data5)  

for ind, obj in enumerate(product):
    for i in variant:
        if obj['prod_variant'] == i['fields']['name']:
            obj['prod_variant'] = i['pk']

    for j in inventorycat:
        if obj['prod_category'] == j['fields']['name']:
            obj['prod_category'] = j['pk']
    
    for k in brand:
        if obj['prod_brand'] == k['fields']['name']:
            obj['prod_brand'] = k['pk']
    
    for l in pkgsize:
        if obj['prod_package_size'] == str(l['fields']['qty'])+l['fields']['unit']:
            obj['prod_package_size'] = l['pk']
    
    for m in unitsize:
        if obj['prod_unit_size'] == str(m['fields']['value'])+m['fields']['unit']:
            obj['prod_unit_size'] = m['pk']
    
    obj['prod_cost'] = 0
    obj['is_active'] = True
    new_obj = {
        "model": "inventory.Product",
        "pk" : ind+1,
        "fields": obj
    }
    new_json_data.append(new_obj)


with open("product.json", "w") as json_file:
    json.dump(new_json_data, json_file)
# %%
