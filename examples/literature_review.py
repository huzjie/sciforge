# -*- coding: utf-8 -*-
"""文献检索 + 综述示例。"""
from sciforge.providers import create
from sciforge.science.literature import LiteratureSearch

if __name__ == "__main__":
    search = LiteratureSearch(create("mock"))
    entries = search.search("深度学习 蛋白质结构预测")
    print(search.synthesize(entries))
