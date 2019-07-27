# Android项目多语言自动化脚本
___

## 目前支持的功能
- [x] 导出项目下所有未翻译的中文字符串到xlsx文件
- [x] 导入翻译后英文字符串到values/strings.xml中，将原有的中文字符串替换掉
- [x] 导入过程中，在将中文字符串替换为翻译的英文字符串之前，会检查values-zh-rCN/strings.xml中是否含有该中文字符串，如果没有就将该中文字符串拷贝过去

## 配置运行环境
1. 安装Python3.x
2. 安装依赖 `pip install -r requirements.txt`


## 使用

### 导出未翻译中文字符串到xlsx文件

Mac, Linux
```bash
chmod a+x export2xls.py
./export2xls.py -p /path/to/android/project
```
Windows
```bash
python export2xls.py -p /path/to/android/project
```

### 导入翻译的英文字符串到Android项目xml文件中

Mac, Linux
```bash
chmod a+x import2xml.py
./export2xls.py -p /path/to/android/project -x /path/to/translated/xlsx/file
```
Windows
```bash
python import2xml.py -p /path/to/android/project -x /path/to/translated/xlsx/file
```

### 查看帮助
```bash
#windows use: python export2xls.py -h
#Mac, Linux
./export2xls.py -h   
Usage: export2xls.py [options]

Options:
  -h, --help            show this help message and exit
  -p /path/to/app/directory, --projectDir=/path/to/app/directory
                        Android project directory. Default value is current
                        directory
  -o OUTPUTDIR, --outputDir=OUTPUTDIR
                        The directory where the xlsx files will be saved.
  -t, --googleTranslate
                        Use google translate the simplified chinese to
                        english.
                        
#windows use: python import2xml.py -h
#Mac, Linux
./import2xml.py -h 
Usage: import2xml.py [options]

Options:
  -h, --help            show this help message and exit
  -p /path/to/app/directory, --projectDir=/path/to/app/directory
                        Android project directory. Default value is current
                        directory
  -x XLSXFILEPATH, --xlsxFilePath=XLSXFILEPATH
                        The translated xlsx file path.
```



    
