from pathlib import Path
import shutil
import subprocess
import sys
import tomllib


def project_version() -> str:
    data = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
    return data["project"]["version"]


def main():
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
    subprocess.run([
        sys.executable, '-m', 'PyInstaller',
        '--name', 'ashare-strategy',
        '--onefile',
        '--collect-all', 'akshare',
        '--collect-all', 'streamlit',
        '--collect-all', 'tinyshare',
        '--add-data', 'config/default_strategy.yaml;config',
        '--add-data', 'src/ashare_strategy/ui/app.py;src/ashare_strategy/ui',
        '--add-data', 'src/ashare_strategy/run_streamlit_app.py;.',
        '--hidden-import', 'ashare_strategy.cli',
        'src/ashare_strategy/cli.py'
    ], check=True)
    out = Path('dist_release')
    out.mkdir(exist_ok=True)
    shutil.copy('dist/ashare-strategy.exe', out / 'ashare-strategy.exe')
    version = project_version()
    archive_name = f'ashare-strategy-windows-x86_64-v{version}'
    shutil.make_archive(archive_name, 'zip', root_dir='dist_release')


if __name__ == '__main__':
    main()
