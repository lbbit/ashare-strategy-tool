from pathlib import Path
import shutil
import subprocess
import sys
import tomllib


ROOT = Path(__file__).resolve().parent


def project_version() -> str:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    return data["project"]["version"]


def main():
    version = project_version()
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True, cwd=ROOT)
    subprocess.run([
        sys.executable, '-m', 'PyInstaller',
        '--name', 'ashare-strategy',
        '--onefile',
        '--collect-all', 'akshare',
        '--collect-all', 'streamlit',
        '--collect-all', 'tinyshare',
        '--hidden-import', 'tinyshare',
        '--add-data', 'config/default_strategy.yaml;config',
        'src/ashare_strategy/cli.py'
    ], check=True, cwd=ROOT)
    subprocess.run([
        sys.executable, '-m', 'PyInstaller',
        '--name', 'run_streamlit_app',
        '--onefile',
        '--collect-all', 'streamlit',
        '--add-data', 'src/ashare_strategy/ui/app.py;.',
        'src/ashare_strategy/run_streamlit_app.py'
    ], check=True, cwd=ROOT)

    out = ROOT / 'dist_release'
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(exist_ok=True)
    runtime_dir = out / 'runtime_data'
    runtime_dir.mkdir(exist_ok=True)

    shutil.copy(ROOT / 'dist' / 'ashare-strategy.exe', out / 'ashare-strategy.exe')
    shutil.copy(ROOT / 'dist' / 'run_streamlit_app.exe', runtime_dir / 'run_streamlit_app.exe')
    shutil.copy(ROOT / 'src' / 'ashare_strategy' / 'ui' / 'app.py', runtime_dir / 'app.py')

    archive_base = ROOT / f'ashare-strategy-windows-x86_64-v{version}'
    archive_path = Path(shutil.make_archive(str(archive_base), 'zip', root_dir=out))
    if not archive_path.exists():
        raise FileNotFoundError(f'Windows release archive not created: {archive_path}')
    print(f'Created Windows archive: {archive_path}')


if __name__ == '__main__':
    main()
