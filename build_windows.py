from pathlib import Path
import shutil
import subprocess
import sys


def main():
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
    subprocess.run([
        sys.executable, '-m', 'PyInstaller',
        '--name', 'ashare-strategy',
        '--onefile',
        '--collect-all', 'akshare',
        '--collect-all', 'streamlit',
        'src/ashare_strategy/cli.py'
    ], check=True)
    out = Path('dist_release')
    out.mkdir(exist_ok=True)
    shutil.copy('dist/ashare-strategy.exe', out / 'ashare-strategy.exe')
    shutil.make_archive('ashare-strategy-windows-x86_64', 'zip', root_dir='dist_release')


if __name__ == '__main__':
    main()
