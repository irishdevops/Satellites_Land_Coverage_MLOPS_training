#!/usr/bin/env python3
import os
import sys
import platform
import shlex
import subprocess
from pathlib import Path

# ---- Config (change if you like) -------------------------------------------
IMAGE = "earth-miner:0.1.0"
CONTAINER = "earth-miner-dev"
DOCKERFILE = "Dockerfile"           # path relative to repo root
BUILD_CONTEXT = "."                 # usually the repo root
MOUNT_IN_CONTAINER = "/app"         # your Dockerfile sets WORKDIR /app
HOST_PORT = "8888"                  # Jupyter host port
CONTAINER_PORT = "8888"             # Jupyter container port
JUPYTER_CMD = (
    "python -m jupyter lab --ip=0.0.0.0 --no-browser "
    "--NotebookApp.allow_origin='*' --NotebookApp.token='' --NotebookApp.password=''"
)
# ---------------------------------------------------------------------------

REPO = Path(__file__).resolve().parent

def run(cmd, check=True, capture=False):
    print(f"> {cmd}")
    if capture:
        return subprocess.run(cmd, shell=True, check=check, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True).stdout.strip()
    else:
        subprocess.run(cmd, shell=True, check=check)

def docker_available():
    try:
        run("docker version", check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def image_exists(image: str) -> bool:
    out = run(f"docker images -q {shlex.quote(image)}", capture=True, check=False)
    return bool(out)

def container_exists(name: str) -> bool:
    out = run(f"docker ps -a --format '{{{{.Names}}}}' | grep -w {shlex.quote(name)}", capture=True, check=False)
    return bool(out)

def container_running(name: str) -> bool:
    out = run(f"docker ps --format '{{{{.Names}}}}' | grep -w {shlex.quote(name)}", capture=True, check=False)
    return bool(out)

def build_image():
    print(f"🛠️  Building image {IMAGE} ...")
    run(f"docker build -t {shlex.quote(IMAGE)} -f {shlex.quote(str(REPO/DOCKERFILE))} {shlex.quote(BUILD_CONTEXT)}")

def remove_container(name: str):
    if container_exists(name):
        if container_running(name):
            run(f"docker rm -f {shlex.quote(name)}")
        else:
            run(f"docker rm {shlex.quote(name)}")

def user_flag():
    # Avoid root-owned files on Linux/macOS; on Windows, skip -u
    if platform.system().lower() in ("linux", "darwin"):
        try:
            uid = os.getuid()
            gid = os.getgid()
            return f"-u {uid}:{gid}"
        except Exception:
            return ""
    return ""

def docker_path(p: Path) -> str:
    # Docker handles POSIX paths; on Windows, Docker Desktop understands "C:\..." too.
    return str(p.resolve())

def run_container():
    vol_mount = f"-v {shlex.quote(docker_path(REPO))}:{MOUNT_IN_CONTAINER}"
    ports = f"-p {HOST_PORT}:{CONTAINER_PORT}"
    name = f"--name {shlex.quote(CONTAINER)}"
    uf = user_flag()

    # We run Jupyter so VS Code can attach to http://localhost:8888
    cmd = (
        f"docker run -it {ports} {vol_mount} {name} {uf} "
        f"-w {MOUNT_IN_CONTAINER} {shlex.quote(IMAGE)} bash -lc {shlex.quote(JUPYTER_CMD)}"
    )
    print("🚀 Starting dev container with your repo mounted and Jupyter Lab running...")
    print(f"   • URL: http://localhost:{HOST_PORT}  (no token)")
    print("   • Stop with Ctrl+C. Container will exit when Jupyter stops.\n")
    run(cmd, check=True)

def ensure_kernel_ready_inside_image():
    """
    Your Dockerfile already does:
      python -m ipykernel install --sys-prefix --name "earth-miner" --display-name "Earth Miner Env"
    and drops a .pth pointing /app.
    So we don't need to install again here.
    This hook is left for completeness if you ever want to extend it.
    """
    pass

def main():
    if not docker_available():
        print("❌ Docker is not available. Please install Docker Desktop / Docker Engine and try again.")
        sys.exit(1)

    # 1) Ensure image exists (build if missing)
    if not image_exists(IMAGE):
        print(f"📦 Image {IMAGE} not found.")
        build_image()
    else:
        print(f"✅ Image {IMAGE} already exists.")

    ensure_kernel_ready_inside_image()

    # 2) (Re)create container cleanly so we always mount the current repo
    if container_exists(CONTAINER):
        print(f"♻️  Removing existing container {CONTAINER} to recreate it cleanly...")
        remove_container(CONTAINER)

    # 3) Run container with the repo mounted and Jupyter Lab started
    run_container()

if __name__ == "__main__":
    main()
