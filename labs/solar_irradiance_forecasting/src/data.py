from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen

import pandas as pd

OPEN_METEO_ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"

HOURLY_VARIABLES = [
    "shortwave_radiation",
    "cloud_cover",
    "temperature_2m",
    "relative_humidity_2m",
    "precipitation",
    "wind_speed_10m",
]


@dataclass(slots=True)
class DatasetConfig:
    """Geography and time window for Open-Meteo archive download."""

    latitude: float = 40.4168
    longitude: float = -3.7038
    start_date: str = "2023-01-01"
    end_date: str = "2023-12-31"
    validation_months: int = 2
    random_seed: int = 42


def _build_archive_url(config: DatasetConfig) -> str:
    params = {
        "latitude": config.latitude,
        "longitude": config.longitude,
        "start_date": config.start_date,
        "end_date": config.end_date,
        "hourly": ",".join(HOURLY_VARIABLES),
        "timezone": "UTC",
    }
    return f"{OPEN_METEO_ARCHIVE_URL}?{urlencode(params)}"


def fetch_open_meteo_hourly(config: DatasetConfig) -> pd.DataFrame:
    """Download hourly archive data from Open-Meteo (UTC)."""
    url = _build_archive_url(config)
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
            "ghi_wm2": hourly["shortwave_radiation"],
            "cloud_cover_pct": hourly["cloud_cover"],
            "temperature_c": hourly["temperature_2m"],
            "relative_humidity_pct": hourly["relative_humidity_2m"],
            "precipitation_mm": hourly["precipitation"],
            "wind_speed_ms": hourly["wind_speed_10m"],
        }
    )
    frame = frame.set_index("timestamp").sort_index()
    return frame


def load_or_build_raw_table(
    processed_dir: Path,
    config: DatasetConfig,
    cache_filename: str = "open_meteo_hourly.parquet",
) -> tuple[pd.DataFrame, Path]:
    """Load cached Parquet or fetch from Open-Meteo and write cache."""
    processed_dir.mkdir(parents=True, exist_ok=True)
    cache_path = processed_dir / cache_filename
    if cache_path.exists():
        frame = pd.read_parquet(cache_path)
        if not isinstance(frame.index, pd.DatetimeIndex):
            frame = frame.set_index("timestamp")
        frame.index = pd.to_datetime(frame.index, utc=True)
        frame = frame.sort_index()
        return frame, cache_path

    frame = fetch_open_meteo_hourly(config)
    frame.to_parquet(cache_path)
    provenance_path = processed_dir / "dataset_provenance.csv"
    provenance = pd.DataFrame(
        [
            {
                "source": "Open-Meteo Archive API",
                "url": OPEN_METEO_ARCHIVE_URL,
                "documentation": "https://open-meteo.com/en/docs/historical-weather-api",
                "latitude": config.latitude,
                "longitude": config.longitude,
                "start_date": config.start_date,
                "end_date": config.end_date,
            }
        ]
    )
    provenance.to_csv(provenance_path, index=False)
    return frame, cache_path


def assign_temporal_split(
    frame: pd.DataFrame,
    validation_months: int,
) -> pd.Series:
    """Label last ``validation_months`` calendar months as validation; rest train."""
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
        "ghi_wm2_median": float(frame["ghi_wm2"].median()),
        "ghi_wm2_p95": float(frame["ghi_wm2"].quantile(0.95)),
    }
