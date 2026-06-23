import pytest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import data_service as ds
import logic


@pytest.fixture(autouse=True)
def clean_data(tmp_path, monkeypatch):
    tmp_file = str(tmp_path / "records.csv")
    monkeypatch.setattr(ds, "DATA_FILE", tmp_file)
    os.makedirs(os.path.dirname(tmp_file), exist_ok=True)
    yield


class TestBug01WhitespaceName:

    def test_leading_trailing_spaces_stripped(self):
        row = ds.add_record("  Bob  ", 7)
        assert row["name"] == "Bob"

    def test_inner_spaces_preserved(self):
        row = ds.add_record(" Ivan Petrov ", 4)
        assert row["name"] == "Ivan Petrov"

    def test_only_spaces_raises(self):
        with pytest.raises(ValueError):
            ds.add_record("    ", 5)


class TestBug02FloatInput:
    def test_float_string_raises_value_error(self):
        with pytest.raises(ValueError):
            logic.parse_guess("3.14")

    def test_float_with_comma_raises_value_error(self):
        with pytest.raises(ValueError):
            logic.parse_guess("50,5")

    def test_float_does_not_count_as_attempt(self):
        outputs = []
        attempts = logic.play_round(
            secret=10,
            get_input=iter(["5.5", "10"]).__next__,
            show_output=outputs.append,
        )
        assert attempts == 1


class TestImp01TopRecords:

    def test_top_n_default_is_10(self):
        for i in range(15):
            ds.add_record(f"Player{i}", i + 1)
        top = logic.get_top_records()
        assert len(top) == 10

    def test_top_n_custom(self):
        for i in range(5):
            ds.add_record(f"Player{i}", i + 1)
        top = logic.get_top_records(top_n=3)
        assert len(top) == 3

    def test_top_sorted_best_first(self):
        ds.add_record("Slow", 20)
        ds.add_record("Fast", 2)
        ds.add_record("Medium", 10)
        top = logic.get_top_records()
        assert top[0]["name"] == "Fast"
        assert top[1]["name"] == "Medium"
        assert top[2]["name"] == "Slow"


class TestChg01FriendlyQuit:
    def test_quit_message_text(self, capsys):
        from menu import main_menu
        inputs = iter(["3"])
        import builtins
        original_input = builtins.input
        builtins.input = lambda _="": next(inputs)
        try:
            main_menu()
        except StopIteration:
            pass
        finally:
            builtins.input = original_input
        captured = capsys.readouterr()
        assert "До свидания" in captured.out