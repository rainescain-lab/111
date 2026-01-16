from __future__ import annotations

import sys

from .config import parse_args
from .exporter import export_csv
from .stats import print_stats
from .tasks import run_tasks


def main() -> int:
    command, settings = parse_args()
    if command == "run":
        run_tasks(settings)
        return 0
    if command == "export":
        export_csv(settings.out_db, settings.out_csv)
        return 0
    if command == "stats":
        print_stats(settings.out_db)
        return 0
    print(f"Unknown command: {command}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
