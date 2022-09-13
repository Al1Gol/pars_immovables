from pandas import DataFrame

from config import *

def export_to_csv(data):
    df = DataFrame(data, columns = [address_field, price_field,\
        organizer_field, name_field, area_field, cadastr_field,\
        encumbrance_field, descr_encum_field, owner_field, \
        type_of_law_field, start_field, finish_field, status_field,\
        subject_field, type_of_property_field, link_field])
    export_csv = df.to_csv('data.csv', index=None, header=True, sep = '|')
