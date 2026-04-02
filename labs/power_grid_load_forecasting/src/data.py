from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen

import pandas as pd

# Redirects to a versioned snapshot (as of 2026, "latest" → 2020-10-06, roughly 2015–2019).
# For years after ~2019, point this URL to a newer OPSD time_series release if available.
OPSD_TIME_SERIES_CSV_URL = (
    "https://data.open-power-system-data.org/time_series/latest/time_series_60min_singleindex.csv"
)
OPEN_METEO_ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"

DEFAULT_LOAD_COLUMN = "DE_load_actual_entsoe_transparency"

HOURLY_WEATHER_VARIABLES = [
    "temperature_2m",
    "relative_humidity_2m",
    "wind_speed_10m",
]


@dataclass(slots=True)
class DatasetConfig:
    """Geography, OPSD column, and time window."""

    latitude: float = 52.52
    longitude: float = 13.405
    start_date: str = "2017-01-01"
    end_date: str = "2018-12-31"
    validation_months: int = 2
    random_seed: int = 42
    load_column: str = DEFAULT_LOAD_COLUMN
    country_code: str = "DE"
    opsd_csv_url: str | None = None


def _build_open_meteo_url(config: DatasetConfig) -> str:
    params = {
        "latitude": config.latitude,
        "longitude": config.longitude,
        "start_date": config.start_date,
        "end_date": config.end_date,
        "hourly": ",".join(HOURLY_WEATHER_VARIABLES),
        "timezone": "UTC",
    }
    return f"{OPEN_METEO_ARCHIVE_URL}?{urlencode(params)}"


def fetch_open_meteo_hourly(config: DatasetConfig) -> pd.DataFrame:
    url = _build_open_meteo_url(config)
    try:
        with urlopen(url, timeout=120) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except URLError as exc:
        raise RuntimeError(f"Open-Meteo request failed: {url}") from exc

    if "hourly" not in payload:
        raise ValueError(f"Unexpected Open-Meteo response keys: {payload.keys()}")

    hourly = payload["hourly"]
    times = pd.to_datetime(hourly["time"], utc=True)
    frame = pd.DataFrame(
        {
            "timestamp": times,
            "temperature_c": hourly["temperature_2m"],
            "relative_humidity_pct": hourly["relative_humidity_2m"],
            "wind_speed_ms": hourly["wind_speed_10m"],
        }
    )
    frame = frame.set_index("timestamp").sort_index()
    return frame


def _filter_window(frame: pd.DataFrame, start: str, end: str) -> pd.DataFrame:
    start_ts = pd.Timestamp(start, tz="UTC")
    end_ts = pd.Timestamp(end + " 23:59:59", tz="UTC")
    return frame.loc[(frame.index >= start_ts) & (frame.index <= end_ts)]


def fetch_opsd_load_hourly(
    config: DatasetConfig,
    chunksize: int = 80_000,
) -> pd.DataFrame:
    """Stream OPSD 60min singleindex CSV and keep one load column in the date window."""
    usecols = ["utc_timestamp", config.load_column]
    start_ts = pd.Timestamp(config.start_date, tz="UTC")
    end_ts = pd.Timestamp(config.end_date + " 23:59:59", tz="UTC")

    chunks: list[pd.DataFrame] = []
    csv_url = config.opsd_csv_url or OPSD_TIME_SERIES_CSV_URL
    for chunk in pd.read_csv(
        csv_url,
        usecols=usecols,
        chunksize=chunksize,
        low_memory=False,
    ):
        chunk["utc_timestamp"] = pd.to_datetime(chunk["utc_timestamp"], utc=True)
        mask = (chunk["utc_timestamp"] >= start_ts) & (chunk["utc_timestamp"] <= end_ts)
        sub = chunk.loc[mask].copy()
        if not sub.empty:
            chunks.append(sub)

    if not chunks:
        raise ValueError(
            f"No OPSD rows in [{config.start_date}, {config.end_date}] for column {config.load_column!r}. "
            "The OPSD 'latest' CSV is a dated snapshot (often ending around 2019); narrow the window or "
            "set OPSD_TIME_SERIES_CSV_URL to a newer release from https://open-power-system-data.org/time_series/."
        )

    out = pd.concat(chunks, ignore_index=True)
    out = out.rename(columns={config.load_column: "load_mw"})
    out = out.dropna(subset=["load_mw"])
    out = out.set_index("utc_timestamp").sort_index()
    out = out[~out.index.duplicated(keep="last")]
    return out


def load_or_build_merged_table(
    processed_dir: Path,
    config: DatasetConfig,
    load_cache_name: str = "opsd_load_filtered.parquet",
    weather_cache_name: str = "open_meteo_hourly.parquet",
    merged_cache_name: str = "load_weather_hourly.parquet",
) -> tuple[pd.DataFrame, Path]:
    """Load cached merged Parquet or build from OPSD + Open-Meteo."""
    processed_dir.mkdir(parents=True, exist_ok=True)
    merged_path = processed_dir / merged_cache_name
    if merged_path.exists():
        frame = pd.read_parquet(merged_path)
        if not isinstance(frame.index, pd.DatetimeIndex):
            frame = frame.set_index("timestamp")
        frame.index = pd.to_datetime(frame.index, utc=True)
        frame = frame.sort_index()
        return frame, merged_path

    load_path = processed_dir / load_cache_name
    if load_path.exists():
        load_frame = pd.read_parquet(load_path)
        if not isinstance(load_frame.index, pd.DatetimeIndex):
            load_frame = load_frame.set_index(load_frame.columns[0])
        load_frame.index = pd.to_datetime(load_frame.index, utc=True)
        load_frame = load_frame.sort_index()
    else:
        load_frame = fetch_opsd_load_hourly(config)
        load_frame.to_parquet(load_path)

    weather_path = processed_dir / weather_cache_name
    if weather_path.exists():
        weather_frame = pd.read_parquet(weather_path)
        if not isinstance(weather_frame.index, pd.DatetimeIndex):
            weather_frame = weather_frame.set_index("timestamp")
        weather_frame.index = pd.to_datetime(weather_frame.index, utc=True)
        weather_frame = weather_frame.sort_index()
    else:
        weather_frame = fetch_open_meteo_hourly(config)
        weather_frame.to_parquet(weather_path)

    load_frame = _filter_window(load_frame, config.start_date, config.end_date)
    weather_frame = _filter_window(weather_frame, config.start_date, config.end_date)

    merged = load_frame.join(weather_frame, how="inner")
    if merged.empty:
        raise ValueError("Merged load+weather frame is empty; check dates and timezone alignment.")

    merged.to_parquet(merged_path)

    provenance_path = processed_dir / "dataset_provenance.csv"
    provenance = pd.DataFrame(
        [
            {
                "source": "OPSD time_series_60min_singleindex",
                "url": config.opsd_csv_url or OPSD_TIME_SERIES_CSV_URL,
                "documentation": "https://open-power-system-data.org/time_series/",
                "load_column": config.load_column,
                "start_date": config.start_date,
                "end_date": config.end_date,
            },
            {
                "source": "Open-Meteo Archive API",
                "url": OPEN_METEO_ARCHIVE_URL,
                "documentation": "https://open-meteo.com/en/docs/historical-weather-api",
                "latitude": config.latitude,
                "longitude": config.longitude,
                "start_date": config.start_date,
                "end_date": config.end_date,
            },
        ]
    )
    provenance.to_csv(provenance_path, index=False)

    return merged, merged_path


def assign_temporal_split(frame: pd.DataFrame, validation_months: int) -> pd.Series:
    if frame.index.tz is None:
        raise ValueError("Expected timezone-aware DatetimeIndex (UTC).")
    last_ts = frame.index.max()
    cutoff = last_ts - pd.DateOffset(months=validation_months)
    split = pd.Series("train", index=frame.index, dtype="string")
    split[frame.index >= cutoff] = "validation"
    return split


def summarize_raw_dataset(frame: pd.DataFrame, split: pd.Series) -> dict[str, object]:
    return {
        "n_rows": int(len(frame)),
        "time_start": frame.index.min().isoformat(),
        "time_end": frame.index.max().isoformat(),
        "split_counts": split.value_counts().to_dict(),
        "load_mw_median": float(frame["load_mw"].median()),
        "load_mw_p95": float(frame["load_mw"].quantile(0.95)),
        "temperature_c_median": float(frame["temperature_c"].median()),
    }
