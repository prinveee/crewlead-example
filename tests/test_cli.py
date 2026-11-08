import json

from tally.cli import main


def test_prints_a_table(tmp_path, capsys):
    path = tmp_path / "data.csv"
    path.write_text("city,price\nParis,3\nLyon,5\n", encoding="utf-8")
    assert main([str(path)]) == 0
    out = capsys.readouterr().out.splitlines()
    assert out[0].split() == ["column", "kind", "count", "min", "max", "mean", "distinct"]
    assert out[1].split() == ["city", "text", "2", "2"]
    assert out[2].split() == ["price", "number", "2", "3", "5", "4"]


def test_missing_file_exits_2(tmp_path, capsys):
    assert main([str(tmp_path / "nope.csv")]) == 2
    assert "nope.csv" in capsys.readouterr().err



def test_json_prints_one_object_per_column_in_file_order(tmp_path, capsys):
    path = tmp_path / "data.csv"
    path.write_text("city,price\nParis,1.123456789\nLyon,2\n", encoding="utf-8")
    assert main(["--json", str(path)]) == 0
    data = json.loads(capsys.readouterr().out)
    assert isinstance(data, list)
    assert [d["name"] for d in data] == ["city", "price"]
    for d in data:
        assert list(d.keys()) == ["name", "kind", "count", "min", "max", "mean", "distinct"]
    assert data[1]["mean"] == (1.123456789 + 2) / 2
    assert data[1]["min"] == 1.123456789
    assert data[1]["max"] == 2


def test_json_number_column_has_number_stats_and_null_distinct(tmp_path, capsys):
    path = tmp_path / "data.csv"
    path.write_text("price\n3\n5\n", encoding="utf-8")
    assert main(["--json", str(path)]) == 0
    column = json.loads(capsys.readouterr().out)[0]
    assert column["kind"] == "number"
    assert column["count"] == 2
    assert column["min"] == 3
    assert column["max"] == 5
    assert column["mean"] == 4
    for key in ("count", "min", "max", "mean"):
        assert isinstance(column[key], (int, float)) and not isinstance(column[key], bool)
    assert column["distinct"] is None


def test_json_text_column_has_distinct_and_null_stats(tmp_path, capsys):
    path = tmp_path / "data.csv"
    path.write_text("city\nParis\nLyon\nParis\n", encoding="utf-8")
    assert main(["--json", str(path)]) == 0
    column = json.loads(capsys.readouterr().out)[0]
    assert column["kind"] == "text"
    assert column["count"] == 3
    assert column["distinct"] == 2
    for key in ("count", "distinct"):
        assert isinstance(column[key], int) and not isinstance(column[key], bool)
    for key in ("min", "max", "mean"):
        assert column[key] is None


def test_json_name_is_exact_header_text(tmp_path, capsys):
    path = tmp_path / "data.csv"
    path.write_text('"say ""hi""",unit price,"a, b",café\n1,2,3,4\n', encoding="utf-8")
    assert main(["--json", str(path)]) == 0
    data = json.loads(capsys.readouterr().out)
    assert [d["name"] for d in data] == ['say "hi"', "unit price", "a, b", "café"]


def test_json_missing_file_exits_2(tmp_path, capsys):
    path = tmp_path / "nope.csv"
    assert main(["--json", str(path)]) == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("tally: ")
    assert captured.err.rstrip("\n").endswith(f": {path}")


def test_table_output_unchanged_without_json(tmp_path, capsys):
    path = tmp_path / "data.csv"
    path.write_text("city,price\nParis,3\nLyon,5\n", encoding="utf-8")
    assert main([str(path)]) == 0
    assert capsys.readouterr().out == (
        "column  kind    count  min  max  mean  distinct\n"
        "city    text    2                      2\n"
        "price   number  2      3    5    4\n"
    )
