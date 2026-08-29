# -*- coding: utf-8 -*-
"""假设生成 + 排序示例。"""
from sciforge.providers import create
from sciforge.science.hypothesis import HypothesisEngine

if __name__ == "__main__":
    engine = HypothesisEngine(create("mock"))
    hyps = engine.generate("运动是否改善认知功能？", n=3)
    for h in engine.rank(hyps):
        print("[%.3f] %s" % (h.score, h.statement))
