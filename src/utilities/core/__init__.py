from __future__ import annotations

from pathlib import Path


def clean_path(path: Path | str, resolve: bool = True) -> Path:
    """Converts a string to a path and resolves it to an absolute location if `resolve` is True

    Parameters
    ----------
    path : Path | str
        Path to resolve
    resolve : bool
        Flag to resolve the path to an absolute position


    Returns
    -------
    Path
        Resolved path object
    """
    if isinstance(path, str):
        path = Path(path)
    if resolve:
        path = path.resolve()
    return path
