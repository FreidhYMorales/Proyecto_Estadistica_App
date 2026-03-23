import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import gmean, hmean


class CentralMeasures:
    """Calculates central tendency measures for grouped data."""

    @staticmethod
    def interpolate(table: pd.DataFrame, n: int, interval: int, percentage: float) -> float:
        """Interpolates a positional measure (quartile, decile, percentile) from a grouped table."""
        pos = n * percentage
        row = table[table["Fa"] >= pos].iloc[0]
        idx = row.name
        L = row["Li"]
        F = table.loc[idx - 1, "Fa"] if idx > 0 else 0
        f = row["f"]
        return L + ((pos - F) / f) * interval if f != 0 else float(L)

    @staticmethod
    def calculate(
        data_list: list,
        table: pd.DataFrame,
        n: int,
        interval: int,
        df: pd.DataFrame,
    ) -> dict:
        """
        Calculates all central tendency measures for grouped data.

        Args:
            data_list: Raw data values.
            table: Grouped frequency table with Li, Ls, Xi o ci, f, Fa columns.
            n: Total number of observations.
            interval: Class interval width.
            df: Raw DataFrame with column 'x'.

        Returns:
            dict with mean, median, mode_raw, mode_interpolated, geometric_mean,
                       harmonic_mean, q1, q2, q3, deciles, percentiles.
        """
        mean = (table["Xi o ci"] * table["f"]).sum() / n

        # Median
        median_pos = n / 2
        row_m = table[table["Fa"] >= median_pos].iloc[0]
        idx_m = row_m.name
        F_m = table.loc[idx_m - 1, "Fa"] if idx_m > 0 else 0
        median = row_m["Li"] + ((median_pos - F_m) / row_m["f"]) * interval

        # Mode (Czuber interpolation)
        f_modal = table["f"].max()
        row_mo = table[table["f"] == f_modal].iloc[0]
        idx_mo = row_mo.name
        f1 = f_modal
        f0 = table.loc[idx_mo - 1, "f"] if idx_mo > 0 else 0
        f2 = table.loc[idx_mo + 1, "f"] if (idx_mo + 1) in table.index else 0
        D1, D2 = f1 - f0, f1 - f2
        mode_interp = (
            row_mo["Li"] + (D1 / (D1 + D2)) * interval if (D1 + D2) != 0 else float(row_mo["Li"])
        )

        # Raw mode(s)
        freq_counts = df["x"].value_counts()
        raw_modes = freq_counts[freq_counts == freq_counts.max()].index.tolist()
        mode_raw = ", ".join(map(str, raw_modes))

        geo_mean = float(gmean(df["x"]))
        harm_mean = float(hmean(df["x"]))

        q1 = CentralMeasures.interpolate(table, n, interval, 0.25)
        q2 = float(median)
        q3 = CentralMeasures.interpolate(table, n, interval, 0.75)

        deciles = {
            f"D{i}": CentralMeasures.interpolate(table, n, interval, i / 10)
            for i in range(1, 10)
        }
        percentiles = {
            f"P{i}": CentralMeasures.interpolate(table, n, interval, i / 100)
            for i in range(1, 100)
        }

        return {
            "mean": float(mean),
            "median": q2,
            "mode_raw": mode_raw,
            "mode_interpolated": float(mode_interp),
            "geometric_mean": geo_mean,
            "harmonic_mean": harm_mean,
            "q1": float(q1),
            "q2": q2,
            "q3": float(q3),
            "deciles": {k: float(v) for k, v in deciles.items()},
            "percentiles": {k: float(v) for k, v in percentiles.items()},
        }


class DispersionMeasures:
    """Calculates dispersion and shape measures for a numeric data list."""

    @staticmethod
    def calculate_dispersion(data: list) -> dict:
        """
        Returns:
            n, mean, variance_population, variance_sample,
            std_population, std_sample, range, min, max, q1, q3, iqr, cv.
        """
        arr = np.array(data, dtype=float)
        mean = np.mean(arr)
        std_sample = np.std(arr, ddof=1)
        q1 = float(np.percentile(arr, 25))
        q3 = float(np.percentile(arr, 75))
        cv = (std_sample / mean * 100) if mean != 0 else 0.0

        return {
            "n": len(arr),
            "mean": float(mean),
            "variance_population": float(np.var(arr, ddof=0)),
            "variance_sample": float(np.var(arr, ddof=1)),
            "std_population": float(np.std(arr, ddof=0)),
            "std_sample": float(std_sample),
            "range": float(np.max(arr) - np.min(arr)),
            "min": float(np.min(arr)),
            "max": float(np.max(arr)),
            "q1": q1,
            "q3": q3,
            "iqr": q3 - q1,
            "cv": float(cv),
        }

    @staticmethod
    def calculate_shape(data: list) -> dict:
        """
        Returns:
            skewness, kurtosis, skewness_label, kurtosis_label.
        """
        arr = np.array(data, dtype=float)
        skewness = float(stats.skew(arr, bias=False))
        kurtosis = float(stats.kurtosis(arr, bias=False))

        if abs(skewness) < 0.5:
            skew_label = "Aproximadamente simétrica"
        elif skewness > 0:
            skew_label = "Asimétrica positiva (cola derecha)"
        else:
            skew_label = "Asimétrica negativa (cola izquierda)"

        if abs(kurtosis) < 0.5:
            kurt_label = "Mesocúrtica (normal)"
        elif kurtosis > 0:
            kurt_label = "Leptocúrtica (más puntiaguda)"
        else:
            kurt_label = "Platicúrtica (más achatada)"

        return {
            "skewness": skewness,
            "kurtosis": kurtosis,
            "skewness_label": skew_label,
            "kurtosis_label": kurt_label,
        }
