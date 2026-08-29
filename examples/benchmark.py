# -*- coding: utf-8 -*-
"""基准评测示例。"""
from sciforge.providers import create
from sciforge.science.benchmark import ScienceBenchmark

if __name__ == "__main__":
    b = ScienceBenchmark(create("mock"))
    results = b.run()
    for r in results:
        print("[%.4f] %s" % (r.score, r.case_id))
