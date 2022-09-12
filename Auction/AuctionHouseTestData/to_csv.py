from pandas import DataFrame

from config import *
from data_parsing import get_data

def export_to_csv():
    df = DataFrame(get_data(), columns = [region_field, type_auction_field,\
        price_field, type_of_object_field, address_field, area_field, contacts_field, documents_field,\
        presentation_field, decript_field, cadastr_field, link_field])
    export_csv = df.to_csv('auction_data.csv', index=None, header=True, sep = '|')
