from openpyxl import load_workbook


def excel_to_dict(file_path, sheet_name):
    workbook = load_workbook(filename=file_path)
    sheet = workbook[sheet_name]

    data = list()

    headers = [cell.value for cell in sheet[1]]

    for row in sheet.iter_rows(min_row=2, values_only=True):
        row_data = dict(zip(headers, row))
        data.append(row_data)

    return data


def get_sheet_names(file_path):
    workbook = load_workbook(filename=file_path)
    sheet_names = workbook.sheetnames

    return sheet_names
