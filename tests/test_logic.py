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


def _make_inputs(*values):
    it = iter(values)
    return lambda: next(it)


class TestGenerateSecret:
    def test_in_default_range(self):
        for _ in range(100):
            n = logic.generate_secret()
            assert logic.MIN_NUMBER <= n <= logic.MAX_NUMBER

    def test_custom_range(self):
        n = logic.generate_secret(1, 5)
        assert 1 <= n <= 5

    def test_equal_bounds_raises(self):
        with pytest.raises(ValueError):
            logic.generate_secret(10, 10)

    def test_inverted_bounds_raises(self):
        with pytest.raises(ValueError):
            logic.generate_secret(50, 10)


class TestCheckGuess:
    def test_correct(self):
        assert logic.check_guess(42, 42) == "correct"

    def test_too_low(self):
        assert logic.check_guess(10, 50) == "too_low"

    def test_too_high(self):
        assert logic.check_guess(90, 50) == "too_high"

    def test_boundary_min(self):
        assert logic.check_guess(logic.MIN_NUMBER, logic.MIN_NUMBER) == "correct"

    def test_boundary_max(self):
        assert logic.check_guess(logic.MAX_NUMBER, logic.MAX_NUMBER) == "correct"

    def test_type_error_on_string(self):
        with pytest.raises(TypeError):
            logic.check_guess("42", 42)


class TestParseGuess:
    def test_valid_integer(self):
        assert logic.parse_guess("50") == 50

    def test_strips_whitespace(self):
        assert logic.parse_guess("  37  ") == 37

    def test_empty_string_raises(self):
        with pytest.raises(ValueError, match="пустым"):
            logic.parse_guess("")

    def test_non_integer_raises(self):
        with pytest.raises(ValueError, match="не целое"):
            logic.parse_guess("abc")

    def test_out_of_range_low_raises(self):
        with pytest.raises(ValueError, match="от"):
            logic.parse_guess("0")

    def test_out_of_range_high_raises(self):
        with pytest.raises(ValueError, match="от"):
            logic.parse_guess("101")

    def test_float_string_raises(self):
        with pytest.raises(ValueError):
            logic.parse_guess("3.14")


class TestGetTopRecords:
    def test_sorted_ascending_by_attempts(self):
        ds.add_record("Charlie", 10)
        ds.add_record("Alice", 3)
        ds.add_record("Bob", 7)
        top = logic.get_top_records()
        assert top[0]["name"] == "Alice"
        assert top[1]["name"] == "Bob"
        assert top[2]["name"] == "Charlie"

    def test_top_n_limits_results(self):
        for i in range(15):
            ds.add_record(f"Player{i}", i + 1)
        top = logic.get_top_records(top_n=10)
        assert len(top) == 10

    def test_empty_returns_empty_list(self):
        assert logic.get_top_records() == []


class TestPlayRound:
    def test_correct_on_first_try(self):
        outputs = []
        attempts = logic.play_round(
            secret=42,
            get_input=_make_inputs("42"),
            show_output=outputs.append,
        )
        assert attempts == 1
        assert any("Верно" in o for o in outputs)

    def test_too_low_then_correct(self):
        outputs = []
        attempts = logic.play_round(
            secret=50,
            get_input=_make_inputs("10", "50"),
            show_output=outputs.append,
        )
        assert attempts == 2
        assert any("мало" in o for o in outputs)

    def test_too_high_then_correct(self):
        outputs = []
        attempts = logic.play_round(
            secret=20,
            get_input=_make_inputs("80", "20"),
            show_output=outputs.append,
        )
        assert attempts == 2
        assert any("много" in o for o in outputs)

    def test_invalid_input_does_not_count(self):
        outputs = []
        attempts = logic.play_round(
            secret=30,
            get_input=_make_inputs("abc", "", "200", "30"),
            show_output=outputs.append,
        )
        assert attempts == 1

    def test_multiple_attempts_counted(self):
        outputs = []
        attempts = logic.play_round(
            secret=55,
            get_input=_make_inputs("1", "2", "3", "55"),
            show_output=outputs.append,
        )
        assert attempts == 4