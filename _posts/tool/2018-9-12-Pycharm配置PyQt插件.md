---
layout: post
title: Pycharm配置PyQt插件
keywords: iTerm2
categories: 工具
---

## 安装PyQt及QtDesigner

使用`pip`安装

```python
pip3 install PyQt5
pip3 install PyQt5-tools
```

## 配置QtDesigner
设计UI界面

![QtDesigner]({{ site.baseurl }}/images/tool/qtdesigner.jpg)

1. Program:
`E:\Anaconda\Anaconda3\Lib\site-packages\pyqt5-tools\designer.exe`
2. Arguments:
不设置参数
3. Working directory:
`$FileDir$`

## 配置PyUIC
PyUIC能将**UI文件***.ui文件转成PyQt能使用的*.py文件

![PyUIC]({{ site.baseurl }}/images/tool/pyuic.jpg)

具体配置如下：

1. Program:
`E:\Anaconda\Anaconda3\python.exe`
2. Arguments:
`-m PyQt5.uic.pyuic  $FileName$ -o $FileNameWithoutExtension$_ui.py`
3. Working directory:
`$FileDir$`

## 配置PyRcc
PyUIC能将**资源文件***.qrc文件转成PyQt能使用的*.py文件

![PyRcc]({{ site.baseurl }}/images/tool/pyrcc.jpg)

1. Program:
`E:\Anaconda\Anaconda3\Scripts\pyrcc5.exe`
2. Arguments:
`$FileName$ -o $FileNameWithoutExtension$_rc.py`
3. Working directory:
`$FileDir$`
