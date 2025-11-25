#!/usr/bin/env python3
import re
import sys
from pathlib import Path

# List of common video extensions
VIDEO_EXTENSIONS = [".mkv", ".mp4", ".avi", ".mov", ".flv", ".wmv", ".webm"]


def rename_sports_file(file_path: Path):
    """
    Rename sports files to format:
    League.YYYY.MM.DD.TeamA.vs.TeamB.ext
    """

    league = file_path.parents[1].name  # e.g. "NCAA" from /NCAA/Season.../
    base_name = file_path.stem
    ext = file_path.suffix.lower()

    if ext not in VIDEO_EXTENSIONS:
        print(f"⚠ Skipping unsupported file type: {file_path.name}")
        return

    # Match "TeamA vs. TeamB DD.MM.YY"
    #    match = re.match(r"(.+?)\s+(\d{2})\.(\d{2})\.(\d{2})$", base_name)
    #    if not match:
    #        print(f"❌ Skipping (no match): {file_path.name}")
    #        return
    #
    #    matchup, day, month, year_suffix = match.groups()

    # Match "TeamA vs TeamB DD.MM.YY" or "TeamA at TeamB DD.MM.YY" with optional prefix
    match = re.search(
        r"([A-Za-z0-9 .-]+?)\s+(vs\.|at|VS|\-|v|vs)\s+([A-Za-z0-9 .-]+)\s+(\d{2})\.(\d{2})\.(\d{2,4})",
        base_name,
    )
    if not match:
        print(f"❌ Skipping (no match): {file_path.name}")
        return

    team1, vs_at, team2, day, month, year = match.groups()

    # Normalize year to 4 digits if only 2 digits
    if len(year) == 2:
        year = "20" + year

    # Clean matchup (replace " vs. " and spaces)
    matchup_clean = f"{team1.replace(' ', '-')}.vs.{team2.replace(' ', '-')}"

    # New filename
    new_name = f"{league}.{year}.{month}.{day}.{matchup_clean}{ext}"
    new_path = file_path.parent / new_name

    # Rename
    file_path.rename(new_path)
    print(f"✅ {file_path.name} -> {new_name}")


def main(target_folder):
    folder = Path(target_folder)
    if not folder.exists():
        print(f"❌ Folder not found: {folder}")
        sys.exit(1)

    for file in folder.iterdir():
        if file.is_file():
            rename_sports_file(file)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python rename_sports.py <folder>")
        sys.exit(1)

    main(sys.argv[1])
