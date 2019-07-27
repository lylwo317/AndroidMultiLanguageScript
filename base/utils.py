import os
import re

from openpyxl.cell import Cell
from openpyxl.worksheet.worksheet import Worksheet


class Utils(object):

    @staticmethod
    def contains_simplified_chinese(string: str):
        if string is None:
            return False
        return re.search("[\u4e00-\u9FFF]", string)

    @staticmethod
    def get_column_index_by_name_in_first_row(sheet: Worksheet, name: str):
        first_row = sheet[1]
        try:
            cell: Cell = next(x for x in first_row if x.value == name)
        except StopIteration:
            raise RuntimeError('first row in \"' + sheet.title + "\" sheet is not contain \"" + name + "\" column")
        return cell.column

    @staticmethod
    def get_all_default_strings_xml_file_path(project_path: str):
        path_list = []
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith("strings.xml") and root.endswith("values"):
                    path_list.append(os.path.join(root, file))
        return path_list
