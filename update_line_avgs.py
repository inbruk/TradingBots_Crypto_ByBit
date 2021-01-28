import pandas as pd
from IPython.core.display import display

def get_cache_filename(symbol_str):
    return r'data/' + symbol_str.lower() + '.csv'

def get_output_filename(symbol_str,suffix):
    return r'data/' + symbol_str.lower() + '_' + suffix + '.csv'


def update_line(symbol_str):

    in_file_name = get_cache_filename(symbol_str)
    in_df = pd.read_csv(in_file_name, header=None)

    out_df = pd.DataFrame(columns=['value'])

    in_df.sort_values(by=['col1'])
    for item in in_df:
        new_value = ( item['open'] + item['high'] + item['low'] + item['close'] ) / 4.0
        new_row = {'value': item['open_time']}
        out_df = out_df.append(new_row, ignore_index=True)


    out_file_name = get_output_filename(symbol_str,'line')
    out_df.to_csv(out_file_name, index=False, header=True)
    return out_df