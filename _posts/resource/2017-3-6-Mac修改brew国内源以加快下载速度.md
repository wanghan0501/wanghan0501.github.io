---
layout: post
title: Mac修改brew国内源以加快下载速度
keywords: Homebrew,源
categories: 资源
---

[Homwbrew](https://brew.sh)是macOS不可或缺的套件管理器，Homebrew 使macOS更完美。使用 gem 来安装 gems、用 brew 来搞定那些依赖包。

<!--more-->

## 简介
因为Homebrew默认的源是GitHub源，在国内因为你懂的原因，下载速度堪忧，顾考虑更换国内源，幸好中科大和清华都提供了brew源，因此我们考虑更换为这两个学校的brew源

## 步骤
* 替换brew.git:

```
cd "$(brew --repo)"
git remote set-url origin https://mirrors.ustc.edu.cn/brew.git

```

* 替换homebrew-core.git:

```
cd "$(brew --repo)/Library/Taps/homebrew/homebrew-core"

git remote set-url origin https://mirrors.ustc.edu.cn/homebrew-core.git

```

* 替换Homebrew Bottles源

```
对于bash用户
echo 'export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.ustc.edu.cn/homebrew-bottles' >> ~/.bash_profile
source ~/.bash_profile

对于zsh用户
echo 'export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.ustc.edu.cn/homebrew-bottles' >> ~/.zshrc
source ~/.zshrc
```
	
* 在中科大源失效或宕机时可以

	1.  参考[清华源设置](https://mirrors.tuna.tsinghua.edu.cn/help/homebrew/)
	
	2.  切换回官方源
			
```
重置brew.git:

cd "$(brew --repo)"git remote set-url origin https://github.com/Homebrew/brew.git

重置homebrew-core.git:
	
cd "$(brew --repo)/Library/Taps/homebrew/homebrew-core"
git remote set-url origin https://github.com/Homebrew/homebrew-core.git
	
注释掉bash配置文件里的有关Homebrew Bottles即可恢复官方源。重启bash或让bash重读配置文件。
```	


