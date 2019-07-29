import sys


class _const(object):
    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:  # 判断是否已经被赋值，如果是则报错
            raise self.ConstError("Can't change const.%s" % name)
        if not name.isupper():  # 判断所赋值是否是全部大写，用来做第一次赋值的格式判断，也可以根据需要改成其他判断条件
            raise self.ConstCaseError('const name "%s" is not all supercase' % name)

        self.__dict__[name] = value


const = _const()
sys.modules[__name__] = const
const.EXPORT_XLSX_FILENAME = "strings.xlsx"
const.EXPORT_TRANSLATE_FILE_NAME = "GoogleTranslateStrings.xlsx"
const.KEY_COLUMN_NAME = 'key'
const.ZH_COLUMN_NAME = 'zh'
const.EN_COLUMN_NAME = 'en'
const.STRINGS_XML_FILE_NAME = 'strings.xml'
