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


def test_empty_cells_do_not_make_a_number_column_text():
    s = summarise_column("items", ["2", "1", "", "3"])
    assert s.kind == "number"
    assert (s.minimum, s.maximum, s.mean) == (1.0, 3.0, 2.0)
    assert s.count == 3


def test_count_skips_empty_cells_in_a_text_column():
    s = summarise_column("city", ["Paris", "", "Lyon"])
    assert s.kind == "text"
    assert s.count == 2


def test_empty_cells_do_not_hide_text():
    s = summarise_column("mixed", ["1", "", "abc"])
    assert s.kind == "text"
