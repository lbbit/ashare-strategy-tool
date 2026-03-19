from __future__ import annotations

from streamlit.web import cli as stcli
import sys

from ashare_strategy.runtime import bundle_root


def main() -> None:
    app_path = bundle_root() / 'src' / 'ashare_strategy' / 'ui' / 'app.py'
    sys.argv = ['streamlit', 'run', str(app_path)]
    raise SystemExit(stcli.main())


if __name__ == '__main__':
    main()
