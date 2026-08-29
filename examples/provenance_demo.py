# -*- coding: utf-8 -*-
"""溯源与重放示例。"""
from sciforge.science.provenance import ProvenanceTracker

if __name__ == "__main__":
    pt = ProvenanceTracker()
    notebook = pt.record("notebook", "原始数据与代码")
    report = pt.record("report", "最终结论", parents=[notebook.id])
    print("report hash:", report.content_hash)
    print("lineage:", [a.kind for a in pt.lineage(report.id)])
