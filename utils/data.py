import xlrd
import json
import yaml
from utils.path import DATA_FILE


class Excel(object):
    def __init__(self, file_path):
        self.wb = xlrd.open_workbook(file_path)

    def get_sheet(self, sheet_name):
        sh = self.wb.sheet_by_name(sheet_name)
        title = sh.row_values(0)
        data = []
        for row in range(1, sh.nrows):
            case_data = sh.row_values(row)
            data.append(dict(zip(title, case_data)))
        return data


def get_data():
    with open(DATA_FILE, encoding='utf-8') as f:
        return yaml.load(f)


if __name__ == '__main__':
    excel = Excel('data.xls')
    data = excel.get_sheet('添加加油卡')
    print(data)
    for case in data:
        print(case['TITLE'])
