import math
import pandas as pd


class Trends:
    """Builds grouped and ungrouped frequency tables from raw data lists."""

    @staticmethod
    def build_grouped_table(data_list: list, interval: int | None = None) -> tuple:
        """
        Constructs a grouped frequency table.

        Uses Sturges' rule (k = 1 + 3.322 * log2(n)) if interval is not provided.
        Returns: (table DataFrame, n, interval, raw DataFrame)
        """
        df = pd.DataFrame({"x": data_list})
        n = len(df)
        xmin, xmax = int(df["x"].min()), int(df["x"].max())

        if interval is None:
            k = round(1 + 3.322 * math.log2(n))
            interval = math.ceil((xmax - xmin) / k)
            if interval < 2:
                interval = 2

        Li = list(range(xmin, xmax + 1, interval))
        Ls = [li + interval - 1 for li in Li]
        if Ls[-1] < xmax:
            Ls[-1] = xmax

        table = pd.DataFrame({"Li": Li, "Ls": Ls})
        table["Xi o ci"] = (table["Li"] + table["Ls"]) / 2
        table["f"] = [
            df[(df["x"] >= Li[i]) & (df["x"] <= Ls[i])].shape[0]
            for i in range(len(Li))
        ]

        return table, n, interval, df

    @staticmethod
    def freq_calculate(table: pd.DataFrame, n: int) -> pd.DataFrame:
        """Adds relative and cumulative frequency columns to a grouped table."""
        table["fr%"] = (table["f"] / n * 100).round(2)
        difference = 100 - table["fr%"].sum()
        table.loc[table.index[-1], "fr%"] += difference
        table["Fa"] = table["f"].cumsum()
        table["Fa%"] = (table["Fa"] / n * 100).round(2)
        table.loc[table.index[-1], "Fa%"] = 100.0
        table["Fd"] = n - table["Fa"].shift(1, fill_value=0)
        table["Fd%"] = (table["Fd"] / n * 100).round(2)
        table.loc[table.index[0], "Fd%"] = 100.0
        return table

    @staticmethod
    def append_totals(table: pd.DataFrame) -> pd.DataFrame:
        """Appends a totals summary row suitable for display."""
        row_total = {
            "Li": "", "Ls": "", "Xi o ci": "",
            "f": table["f"].sum(),
            "fr%": f"{round(table['fr%'].sum(), 2)}%",
            "Fa": "", "Fa%": "", "Fd": "", "Fd%": "",
        }
        return pd.concat([table, pd.DataFrame([row_total])], ignore_index=True)

    @staticmethod
    def build_ungrouped_table(data_list: list) -> pd.DataFrame:
        """Builds a non-grouped frequency table for individual data values."""
        df = pd.DataFrame({"x": data_list})
        n = len(df)
        freq = df["x"].value_counts().sort_index()

        fd = (n - freq.cumsum().shift(1, fill_value=0)).tolist()

        return pd.DataFrame({
            "x": freq.index.tolist(),
            "f": freq.values.tolist(),
            "fr%": ((freq / n) * 100).round(2).tolist(),
            "Fa": freq.cumsum().tolist(),
            "Fa%": ((freq.cumsum() / n) * 100).round(2).tolist(),
            "Fd": fd,
            "Fd%": ((pd.Series(fd) / n) * 100).round(2).tolist(),
        })
