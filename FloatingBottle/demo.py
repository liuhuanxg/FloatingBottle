# -*- coding: utf-8 -*-
"""
@Time       :2020/11/13 17:56
@Author     :liuhuan
@verssion   :v1.0
@effect     :TODO
"""
import re
s = "：郑涛)"
pattern = "：(.*)\)"
s1 = re.compile(pattern)
print(s1.findall(s))