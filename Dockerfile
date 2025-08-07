FROM osgeo/gdal:ubuntu-small-3.6.2

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    VENV_PATH=/opt/venv \
    GDAL_CONFIG=/usr/bin/gdal-config \
    CPLUS_INCLUDE_PATH=/usr/include/gdal \
    C_INCLUDE_PATH=/usr/include/gdal

# Toolchain + venv support
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential \
      python3-dev \
      python3-venv \
  && rm -rf /var/lib/apt/lists/*

# Create venv and upgrade pip/setuptools/wheel
RUN python3 -m venv $VENV_PATH && $VENV_PATH/bin/pip install --upgrade pip setuptools wheel
ENV PATH="$VENV_PATH/bin:$PATH"

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python -m ipykernel install --sys-prefix --name "earth-miner" --display-name "Earth Miner Env" || true

RUN python - <<'PY'
import site, pathlib
path = pathlib.Path(site.getsitepackages()[0]) / 'earth_miner_path.pth'
path.write_text('/app')
PY

CMD ["bash"]
