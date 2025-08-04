#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path
import venv

PROJECT_DIR = Path(__file__).parent.resolve()
VENV_DIR     = PROJECT_DIR / ".venv"
ENV_FILE     = PROJECT_DIR / ".env"
REQ_FILE     = PROJECT_DIR / "requirements.txt"
py = sys.executable
def load_env(env_path: Path):
    if not env_path.exists():
        return
    print(f"🔄 Loading .env from {env_path}")
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        os.environ[key] = val

def run(cmd, capture_output=False, **kwargs):
    print(f"> {cmd}")
    if capture_output:
        return subprocess.check_output(cmd, shell=True, text=True, **kwargs)
    else:
        subprocess.check_call(cmd, shell=True, **kwargs)

def main():
    # 1) Create venv if missing
    if not VENV_DIR.exists():
        print(f"⚙️  Creating virtualenv at {VENV_DIR}")
        venv.EnvBuilder(with_pip=True).create(VENV_DIR)
    else:
        print(f"🔁 Using existing virtualenv at {VENV_DIR}")

    # Path to venv’s python
    py = VENV_DIR / ("Scripts/python.exe" if os.name == "nt" else "bin/python")

    # 2) Install deps
    print("📦 Installing dependencies…")
    run(f"{py} -m pip install --upgrade pip setuptools wheel ipykernel")
    if REQ_FILE.exists():
        run(f"{py} -m pip install --no-deps -r {REQ_FILE}")

    # 3) Load .env
    load_env(ENV_FILE)

    # 4) Register the kernel at user level
    print("🔧 Registering Jupyter kernel as 'Earth Miner Env'…")
    run(f'{py} -m ipykernel install --sys-prefix --name earth-miner --display-name "Earth Miner Env"')

    print("✅ Done! 'Earth Miner Env' kernel available in Jupyter or VS Code.")
    
    # 5) Add project root to sys.path using .pth file
    print("🧩 Linking project to site-packages for import access…")
    site_packages = run(f'{py} -c "import site; print(site.getsitepackages()[0])"', capture_output=True).strip()
    pth_path = Path(site_packages) / "earth_miner_path.pth"
    pth_path.write_text(str(PROJECT_DIR))


if __name__ == "__main__":
    main()
