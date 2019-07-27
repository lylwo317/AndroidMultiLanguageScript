#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019-07-27 16:28
# @Author   : Kevin Xie
# @Email    : lylwo317@gmail.com

from optparse import OptionParser
from pathlib import Path

from bs4 import BeautifulSoup, Tag
import re
import openpyxl
import os

from base import const
from base.utils import Utils

zh_cn_dir = "values-zh-rCN"

orig_prettify = BeautifulSoup.prettify
r = re.compile(r'^(\s*)', re.MULTILINE)


def prettify(self, encoding=None, formatter="minimal", indent_width=4):
    return r.sub(r'\1' * indent_width, orig_prettify(self, encoding, formatter))


BeautifulSoup.prettify = prettify


def add_parser():
    parser = OptionParser()

    parser.add_option("-p", "--projectDir",
                      help="Android project directory. Default value is current directory",
                      default=".",
                      metavar="/path/to/app/directory")

    parser.add_option("-x", "--xlsxFilePath",
                      default=const.EXPORT_XLSX_FILENAME,
                      help="The translated xlsx file path.")

    options, args = parser.parse_args()
    print("options: %s, args: %s" % (options, args))
    return options


def read_xls(file_path):
    if not os.path.exists(file_path):
        return
    wb = openpyxl.load_workbook(file_path)
    android_sheet = wb['Android']

    key_column = Utils.get_column_index_by_name_in_first_row(android_sheet, const.KEY_COLUMN_NAME)
    all_rows = {}
    for row in android_sheet.rows:
        all_rows[row[key_column - 1].value] = row
    return android_sheet, all_rows


def import_to_xml(xlsx_file_path: str):
    android_sheet, all_rows = read_xls(xlsx_file_path)
    for path in Utils.get_all_default_strings_xml_file_path(options.projectDir):

        zh_cn_soup, zh_cn_strings_xml_path = get_zh_soup(path)
        if zh_cn_soup is None:
            print(zh_cn_strings_xml_path, "is not exist")
            # 不存在就不需要翻译了
            continue

        default_soup = BeautifulSoup(open(path, encoding='utf-8'), "xml")
        all_string = default_soup.find_all('string')

        zh_column = Utils.get_column_index_by_name_in_first_row(android_sheet, const.ZH_COLUMN_NAME)
        en_column = Utils.get_column_index_by_name_in_first_row(android_sheet, const.EN_COLUMN_NAME)
        zh_index = zh_column - 1
        en_index = en_column - 1
        row_size = 3

        for str_tmp in all_string:
            if Utils.contains_simplified_chinese(str(str_tmp.next)):
                key = str_tmp.attrs['name']
                if key in all_rows:
                    row: tuple = all_rows[key]
                    if en_index <= len(row) - 1 and row[en_index].value is not None:
                        tag_zh_string: Tag = zh_cn_soup.find("string", {"name": key})
                        if tag_zh_string is None:
                            # 检测values-zh-rCN/strings.xml中有没有这个key（字段)），没有就将中文拷贝过去
                            tag_resource: Tag = zh_cn_soup.find('resources')
                            new_tag: Tag = zh_cn_soup.new_tag(str_tmp.name, attrs=str_tmp.attrs)
                            new_tag.string = str_tmp.string
                            tag_resource.append(new_tag)
                        str_tmp.string.replaceWith(row[en_index].value)  # 用英文替换中文
                        print("name:", str_tmp.attrs['name'], " value:", str_tmp.next.__str__())

        all_string_array = default_soup.find_all('string-array')
        for str_tmp in all_string_array:
            index = 0
            for tag_item in str_tmp.find_all('item'):
                if Utils.contains_simplified_chinese(str(tag_item.next)):
                    key = str_tmp.attrs['name'] + "_" + str(index)
                    if key in all_rows:
                        row = all_rows[key]
                        if en_index <= len(row) - 1 and row[en_index].value is not None:
                            tag_item.string = row[en_index].value
                            print("name:", key, "value:", str(tag_item.next))
                index += 1
        save_soup(default_soup, path)
        if os.path.exists(zh_cn_strings_xml_path):
            save_soup(zh_cn_soup, zh_cn_strings_xml_path)


def get_zh_soup(path: str):
    values_dir_parent = Path(path).parent.parent
    zh_cn_soup = None
    zh_cn_strings_xml_path = values_dir_parent / zh_cn_dir / const.STRINGS_XML_FILE_NAME
    if os.path.exists(zh_cn_strings_xml_path):
        zh_cn_soup = BeautifulSoup(open(zh_cn_strings_xml_path, encoding='utf-8'), 'xml')
    return zh_cn_soup, zh_cn_strings_xml_path


def save_soup(default_soup, path):
    with open(path, "w", encoding='utf-8') as file:
        unformatted_tag_list = []

        for i, tag in enumerate(default_soup.find_all(['string', 'item'])):
            unformatted_tag_list.append(str(tag))
            tag.replace_with('{' + 'unformatted_tag_list[{0}]'.format(i) + '}')

        pretty_markup = default_soup.prettify().format(unformatted_tag_list=unformatted_tag_list)
        file.write(pretty_markup)


if __name__ == '__main__':
    options = add_parser()
    import_to_xml(options.xlsxFilePath)
    # getAllStringFilePath()
