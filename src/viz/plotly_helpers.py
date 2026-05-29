"""Optional plotly helpers for interactive figure validation."""

from __future__ import annotations

from typing import List, Optional


def plotly_title_text(fig_json: dict) -> str:
    """Extract plot title text across plotly layout versions."""
    title = fig_json.get("layout", {}).get("title", "")
    if isinstance(title, dict):
        return str(title.get("text", ""))
    return str(title)


def plotly_trace_values(trace: dict, key: str) -> Optional[List[float]]:
    """Return trace axis values when plotly JSON uses plain lists (not binary)."""
    raw = trace.get(key)
    if raw is None or isinstance(raw, dict):
        return None
    return [float(v) for v in raw]
