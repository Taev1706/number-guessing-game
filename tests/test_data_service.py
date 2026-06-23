import pytest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import data_service as ds


@pytest.fixture(autouse=True)
def clean_data(tmp_path, monkeypatch):
    tmp_file = str(tmp_path / "records.csv")
    monkeypatch.setattr(ds, "DATA_FILE", tmp_file)
    os.makedirs(os.path.dirname(tmp_file), exist_ok=True)
    yield


class TestAddRecord:
    def test_add_basic(self):
        row = ds.add_record("Alice", 5)
        assert row["name"] == "Alice"
        assert int(row["attempts"]) == 5

    def test_add_multiple(self):
        ds.add_record("Alice", 5)
        ds.add_record("Bob", 3)
        rows = ds.load_all()
        assert len(rows) == 2

    def test_add_strips_whitespace(self):
        row = ds.add_record("  Bob  ", 7)
        assert row["name"] == "Bob"

    def test_add_empty_name_raises(self):
        with pytest.raises(ValueError, match="пустым"):
            ds.add_record("", 5)

    def test_add_whitespace_name_raises(self):
        with pytest.raises(ValueError):
            ds.add_record("   ", 5)

    def test_add_zero_attempts_raises(self):
        with pytest.raises(ValueError, match="положительным"):
            ds.add_record("Alice", 0)

    def test_add_negative_attempts_raises(self):
        with pytest.raises(ValueError):
            ds.add_record("Alice", -1)

    def test_add_float_attempts_raises(self):
        with pytest.raises(ValueError):
            ds.add_record("Alice", 3.5)


class TestLoadAll:
    def test_load_empty(self):
        rows = ds.load_all()
        assert rows == []

    def test_load_persists_between_calls(self):
        ds.add_record("Alice", 5)
        loaded = ds.load_all()
        assert len(loaded) == 1
        assert loaded[0]["name"] == "Alice"

    def test_load_all_returns_correct_attempts(self):
        ds.add_record("Charlie", 8)
        loaded = ds.load_all()
        assert int(loaded[0]["attempts"]) == 8


class TestClearAll:
    def test_clear_removes_all(self):
        ds.add_record("Alice", 5)
        ds.clear_all()
        assert ds.load_all() == []

    def test_clear_on_empty_no_error(self):
        ds.clear_all()
        assert ds.load_all() == []