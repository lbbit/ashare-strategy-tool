from __future__ import annotations

from streamlit.web import cli as stcli
import sys
from pathlib import Path

from ashare_strategy.runtime import bundle_root, is_frozen


def main() -> None:
    app_path = bundle_root() / 'src' / 'ashare_strategy' / 'ui' / 'app.py'
    if is_frozen() and not app_path.exists():
        app_path = Path(sys.executable).resolve().parent / 'runtime_data' / 'app.py'
    sys.argv = ['streamlit', 'run', str(app_path)]
    raise SystemExit(stcli.main())


if __name__ == '__main__':
    main()
