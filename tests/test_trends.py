import pytest
from utils.trends import Trends

DATA = [10, 12, 14, 15, 16, 18, 20, 21, 22, 25, 26, 28, 30]


class TestBuildGroupedTable:
    def setup_method(self):
        self.table, self.n, self.interval, self.df = Trends.build_grouped_table(DATA)

    def test_n_matches_data_length(self):
        assert self.n == len(DATA)

    def test_interval_is_positive(self):
        assert self.interval > 0

    def test_all_data_covered(self):
        assert self.table["Li"].min() <= min(DATA)
        assert self.table["Ls"].max() >= max(DATA)

    def test_frequencies_sum_to_n(self):
        assert self.table["f"].sum() == self.n

    def test_midpoints_between_limits(self):
        for _, row in self.table.iterrows():
            assert row["Li"] <= row["Xi o ci"] <= row["Ls"]


class TestFreqCalculate:
    def setup_method(self):
        table, n, _, _ = Trends.build_grouped_table(DATA)
        self.table = Trends.freq_calculate(table, n)
        self.n = n

    def test_cumulative_freq_ends_at_n(self):
        assert self.table["Fa"].iloc[-1] == self.n

    def test_cumulative_pct_ends_at_100(self):
        assert self.table["Fa%"].iloc[-1] == pytest.approx(100.0)

    def test_first_descending_freq_equals_n(self):
        assert self.table["Fd"].iloc[0] == self.n

    def test_first_descending_pct_equals_100(self):
        assert self.table["Fd%"].iloc[0] == pytest.approx(100.0)

    def test_relative_freq_sums_to_100(self):
        assert self.table["fr%"].sum() == pytest.approx(100.0, abs=0.1)


class TestBuildUngroupedTable:
    def test_basic_structure(self):
        data = [1, 2, 2, 3, 3, 3]
        result = Trends.build_ungrouped_table(data)
        assert list(result["x"]) == [1, 2, 3]
        assert list(result["f"]) == [1, 2, 3]

    def test_cumulative_freq_ends_at_n(self):
        result = Trends.build_ungrouped_table(DATA)
        assert result["Fa"].iloc[-1] == len(DATA)

    def test_relative_pct_sums_to_100(self):
        result = Trends.build_ungrouped_table(DATA)
        assert result["fr%"].sum() == pytest.approx(100.0, abs=0.1)

    def test_descending_freq_starts_at_n(self):
        result = Trends.build_ungrouped_table(DATA)
        assert result["Fd"].iloc[0] == len(DATA)
