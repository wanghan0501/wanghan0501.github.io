---
layout: post
title: Python词云包wordcloud入门
keywords: Python,词云
categories: 技术
---

构建词云的方法很多, 但是个人觉得python的wordcloud包功能最为强大,可以自定义颜色以及图片。下面简单介绍下wordcloud包用法。

<!--more-->
## 下载链接

官网: [https://amueller.github.io/word_cloud/](https://amueller.github.io/word_cloud/)

github: [https://github.com/amueller/word_cloud](https://github.com/amueller/word_cloud)

## 安装简介

**方法1：pip安装**

对于python2

```bash
pip install wordcloud
```

对于python3

```bash
pip3 install wordcloud
```

**方法2：GitHub源码安装**

* 下载并解压

```bash
wget https://github.com/amueller/word_cloud/archive/master.zipunzip master.ziprm master.zipcd word_cloud-master
```

* 安装依赖包

```bash
sudo pip install -r requirements.txt
```

* 安装wordcloud

```bash
python setup.py install
```



## 代码实例
```python
from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

# 获取当前文件路径
# __file__ 为当前文件, 在ide中运行此行会报错,可改为
# d = path.dirname('.')
d = path.dirname(__file__)

# 读取文本 alice.txt 在包文件的example目录下
#内容为
"""
Project Gutenberg's Alice's Adventures in Wonderland, by Lewis Carroll

This eBook is for the use of anyone anywhere at no cost and with
almost no restrictions whatsoever.  You may copy it, give it away or
re-use it under the terms of the Project Gutenberg License included
with this eBook or online at www.gutenberg.org
"""
text = open(path.join(d, 'alice.txt')).read()

# read the mask / color image
# taken from http://jirkavinse.deviantart.com/art/quot-Real-Life-quot-Alice-282261010
# 设置背景图片
alice_coloring = imread(path.join(d, "alice_color.png"))

wc = WordCloud(background_color="white",  # 背景颜色max_words=2000,# 词云显示的最大词数
               mask= alice_coloring,  # 设置背景图片
               stopwords=STOPWORDS.add("said"),
               max_words=1000,
               max_font_size=100,  # 字体最大值
               min_font_size=10,
               font_path='/Library/Fonts/Songti.ttc', # 设置字体路径，如不设置中文会出现乱码
               random_state=42)
# 生成词云, 可以用generate输入全部文本(中文不好分词),也可以我们计算好词频后使用generate_from_frequencies函数
wc.generate(text)
# wc.generate_from_frequencies(txt_freq)
# txt_freq例子为[('词a', 100),('词b', 90),('词c', 80)]
# 从背景图片生成颜色值
image_colors = ImageColorGenerator(alice_coloring)

# 以下代码显示图片
plt.imshow(wc)
plt.axis("off")
# 绘制词云
plt.figure()
# recolor wordcloud and show
# we could also give color_func=image_colors directly in the constructor
plt.imshow(wc.recolor(color_func=image_colors))
plt.axis("off")
# 绘制背景图片为颜色的图片
plt.figure()
plt.imshow(alice_coloring, cmap=plt.cm.gray)
plt.axis("off")
plt.show()
# 保存图片
wc.to_file(path.join(d, "名称.png"))
```

## 代码效果
词云模版原图

![原图]({{site.baseurl}}/images/tech/alice.png)

词云效果图（1）

![效果图1]({{site.baseurl}}/images/tech/alice_1.png)

词云效果图（2）

![效果图2]({{site.baseurl}}/images/tech/alice_2.png)
