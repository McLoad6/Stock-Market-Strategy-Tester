import file_handler


test = file_handler.get_dict_from_csv('DAX1min.csv')
filled_dict = file_handler.filling_missing_rows(test)
file_handler.write_dict_to_csv('cleaned.csv',filled_dict)
