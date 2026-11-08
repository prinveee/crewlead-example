from tally.stats import summarise, summarise_column


def test_numeric_column_gets_min_max_mean():
    s = summarise_column("price", ["3", "1.5", "4.5"])
    assert s.kind == "number"
    assert (s.minimum, s.maximum, s.mean) == (1.5, 4.5, 3.0)
    assert s.count == 3


def test_text_column_counts_distinct_values():
    s = summarise_column("city", ["Paris", "Lyon", "Paris"])
    assert s.kind == "text"
    assert s.distinct == 2


def test_summarise_keeps_header_order():
    rows = [{"b": "1", "a": "x"}]
    assert [s.name for s in summarise(rows, ["b", "a"])] == ["b", "a"]
