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
