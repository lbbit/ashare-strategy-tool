from pathlib import Path
import shutil
import subprocess
import sys
import tomllib


def project_version() -> str:
    data = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
    return data["project"]["version"]


def main():
    version = project_version()
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
    subprocess.run([
        sys.executable, '-m', 'PyInstaller',
        '--name', 'ashare-strategy',
        '--onefile',
        '--collect-all', 'akshare',
        '--collect-all', 'streamlit',
        '--collect-all', 'tinyshare',
        '--add-data', 'config/default_strategy.yaml;config',
        'src/ashare_strategy/cli.py'
    ], check=True)
    subprocess.run([
        sys.executable, '-m', 'PyInstaller',
        '--name', 'run_streamlit_app',
        '--onefile',
        '--collect-all', 'streamlit',
        '--add-data', 'src/ashare_strategy/ui/app.py;.',
        'src/ashare_strategy/run_streamlit_app.py'
    ], check=True)

    out = Path('dist_release')
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(exist_ok=True)
    runtime_dir = out / 'runtime_data'
    runtime_dir.mkdir(exist_ok=True)

    shutil.copy('dist/ashare-strategy.exe', out / 'ashare-strategy.exe')
    shutil.copy('dist/run_streamlit_app.exe', runtime_dir / 'run_streamlit_app.py')
    shutil.copy('src/ashare_strategy/ui/app.py', runtime_dir / 'app.py')

    archive_name = f'ashare-strategy-windows-x86_64-v{version}'
    shutil.make_archive(archive_name, 'zip', root_dir='dist_release')
