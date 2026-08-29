# -*- coding: utf-8 -*-
from sciforge.science.provenance import ProvenanceTracker


def test_record_hash():
    pt = ProvenanceTracker()
    a = pt.record("report", "hello")
    assert len(a.content_hash) == 64


def test_lineage():
    pt = ProvenanceTracker()
    a = pt.record("notebook", "x")
    b = pt.record("report", "y", parents=[a.id])
    lineage = pt.lineage(b.id)
    assert len(lineage) == 2
