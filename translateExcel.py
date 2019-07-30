#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019-07-29 15:02
# @Author   : Kevin Xie
# @Email    : lylwo317@gmail.com
import os
import re
import time
from optparse import OptionParser

import openpyxl
from googletrans import Translator
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet

customize_dict = {"中": "Medium"}


def add_parser():
    parser = OptionParser()

    parser.add_option("-f", "--flieExcel",
                      help="需要进行翻译的excel 文件",
                      default="",
                      metavar="/path/to/excel")

    options, args = parser.parse_args()
    print("options: %s, args: %s" % (options, args))
    return options


def contains_simplified_chinese(string: str):
    if string is None:
        return False
    return re.search("[\u4e00-\u9FFF]", string)


def translate_xlsx(untranslate_xlsx_file_path):
    if not os.path.exists(untranslate_xlsx_file_path):
        return
    translator = Translator(service_urls=[
        'translate.google.cn'
    ])
    wb: Workbook = openpyxl.load_workbook(untranslate_xlsx_file_path)
    zh_to_en = customize_dict
    max_count = 20
    try:
        count = 0
        for sheet_name in wb.sheetnames:
            sheet_temp: Worksheet = wb.get_sheet_by_name(sheet_name)
            if contains_simplified_chinese(sheet_temp.title):
                temp_title = translator.translate(sheet_temp.title).text
                if len(temp_title) > 30:
                    temp_title = temp_title[:30]
                sheet_temp.title = temp_title
            for col in sheet_temp.columns:
                for cell in col:
                    if cell.value is not None and isinstance(cell.value, str) and contains_simplified_chinese(
                            cell.value):
                        zhStr = cell.value
                        enStr = zh_to_en.get(zhStr)
                        if enStr is None:
                            cell.value = translator.translate(cell.value).text
                            zh_to_en[zhStr] = cell.value
                            count += 1
                            if count == max_count:
                                count = 0
                                time.sleep(30)#控制调用频率
                        else:
                            cell.value = enStr
                        print("zh =", zhStr, " en =", cell.value)
    finally:
        wb.save(untranslate_xlsx_file_path)


if __name__ == '__main__':
    options = add_parser()
    translate_xlsx(options.flieExcel)
