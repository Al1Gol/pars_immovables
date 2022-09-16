from pandas import DataFrame

from config import *

def export_to_csv(data):
    df = DataFrame(data, columns = [data_auc_field, name_field,\
        cadastr_field, address_field, category_field, type_of_use_field,\
        area_field, water_field, drainage_field, warm_field,\
        gas_field, start_price_field, last_day_field, sale_result_field,\
        note_field, documents_field, url_field])
    export_csv = df.to_csv('data.csv', index=None, header=True, sep = '|')
