---
layout: post
title: TensorFlow编程中踩过的坑(1)
keywords: 编程,tensorflow
categories: 技术
---

## 前言
使用TensorFlow框架跑神经网络模型过去了近2个月了，虽不能说熟练掌握，但也略有心得，中间也踩过很多坑，今天就细数下编程中踩过的坑。

## 踩过的坑

1. 优化器`AdadeltaOptimizer`的学习率设置问题

	`AdadeltaOptimizer`是`tf.train`包中的一个优化器，它可以**自动调整学习率**。最开始的时候我看到这个优化器觉得很厉害的一个，结果使用后发现loss根本不下降，本来还以为是用法用错了呢，几经周折，最后才发现是学习率设置的问题。
	
	```python
	# set optimizer
optimizer = tf.train.AdadeltaOptimizer()
# set train_op
train_op = slim.learning.create_train_op(loss, optimizer)
	```
	
	`AdadeltaOptimizer`优化器默认的`learning_rate=0.001`，非常的小，导致梯度下降速度非常慢，最后的解决方案是：提高学习率
	
	```python
	# set optimizer
optimizer = tf.train.AdadeltaOptimizer(learning_rate=1)
# set train_op
train_op = slim.learning.create_train_op(loss, optimizer)
	```

2. `batch_norm_decay`参数设置的问题
	
	`batch norm` 是Google大佬15年提出来的一个用于提高CNN网络性能的正则方法，它的具体内容就不细说了，在这里留下它的论文链接。
	
	我踩到了一个很神奇的坑。
	`batch norm`需要设置一个名为`batch_norm_decay`的参数，它的默认参数是0.997，我当时没有改变这个参数，导致一个神奇的问题:在训练集上精确率在99%了，在测试集上精确率还在50%徘徊。这个神奇的问题困扰了我很久，最后多方请教后才解决。
	
	问题在于，`batch norm`在训练的时候使用的是mini_batch的均值和方差来估计整个数据集的分布，这没有问题。但是在测试的时候，需要根据训练集估计出来一个合适的均值和方差来调整训练集的分布，**那么问题来了：如何算测试集的均值和方差呢？**
	
	论文中采用的是`batch_norm_decay`的方法，可以简单的描述为下式:
	
	$$a_{avg} = \lambda a_m+(1-\lambda)a_{m+1}$$
	
	其中的$\lambda$就是所说的`batch_norm_decay`,如果它设置的太小，测试集上的均值的收敛速度就非常慢，而我的训练数据又非常小，导致测试集上精确率无法提高。
	
	问题的解决方法就是：减小`batch_norm_decay`的值，我设置为0.95，顺利解决了问题。
	
## 后记
不得不说，TensorFlow中的坑是真多，一点点采坑，一点点学习。以后有新的体悟了再更新。

## 资料

- slim: slim是对TensorFlow底层api的进一步封装，官网上的`tensorflow/models`仓库中的slim包的很深，每次查找起来很是不方便，我把它单独提出来了重新上传为一个新库，有兴趣的可以使用它。
	- slim模型地址: [https://github.com/wanghan0501/slim](https://github.com/wanghan0501/slim)
	- slim源代码地址: [https://github.com/tensorflow/tensorflow/tree/master/tensorflow/contrib/slim](https://github.com/tensorflow/tensorflow/tree/master/tensorflow/contrib/slim)
- AdadeltaOptimizer: 官方API文档地址: [https://www.tensorflow.org/versions/master/api_docs/python/tf/train/AdadeltaOptimizer](https://www.tensorflow.org/versions/master/api_docs/python/tf/train/AdadeltaOptimizer)

- Batch Normalization: Accelerating Deep Network Training by
Reducing Internal Covariate Shift: [https://proceedings.mlr.press/v37/ioffe15.html](https://proceedings.mlr.press/v37/ioffe15.html)
