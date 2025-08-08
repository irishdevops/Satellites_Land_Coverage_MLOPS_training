This repo contains customized functions that allow you to train models for satellital imagery by data mining images from earth engine. The user needs a query with layer coordinates.




### **Instructions**

1 - Install Docker and create image. <br>

2 - Notebookare used for training the models from a .jpeg collection. Therefore, both notebooks are indepdendant and can be used separately. <br>
<br>
Note: You will need to have an active earth engine account and an active project to connect for the data mining process. https://earthengine.google.com/<br>
<br>
Note: Following the oficial earthengine api is recommended as complementay source code: https://github.com/google/earthengine-api

### **Advantages and unique value:**

- Use data mining and train geospatial models all in one! Try this computer vision experiment. you can choose the pre-trained suggested models from tensorflow and pytorch or use your own models.


## 🛠️ System Requirements

Before running `setup.py`, make sure the following system dependencies are installed:

### macOS
```sh
brew install gdal
```

```Ubuntu
sudo apt-get update && sudo apt-get install -y gdal-bin libgdal-dev
```

```Windows
Use OSGeo4W

Or install via conda: conda install -c conda-forge gdal
```

# 🌍 Earth Miner Development Environment

This guide explains how to set up and run the **Earth Miner** development environment using Docker and VS Code Dev Containers.  
It works on **Windows**, **macOS**, and **Linux**.

---

# Earth Miner Dev – Docker Setup Instructions 🐳

This README explains how to install Docker, build the development image, and run it in Visual Studio Code using a Dev Container.

---

## 1. Install Docker

You must have Docker installed and running on your machine.

**MacOS**  
1. Download Docker Desktop from: https://www.docker.com/products/docker-desktop  
2. Open the `.dmg` file and drag Docker to Applications.  
3. Open Docker Desktop, complete the setup prompts, and make sure the whale icon appears in your menu bar.

**Windows**  
1. Download Docker Desktop from: https://www.docker.com/products/docker-desktop  
2. Install it.  
3. Ensure "Use WSL 2 based engine" is enabled during setup.  
4. Start Docker Desktop from the Start Menu and keep it running.


## 2. Build the Docker image - Open the terminal inside the code repository and run
 !Before executing, make sure your Docker app is open!
```bash
docker build --no-cache -t earth-miner:0.1.0 .
```
Now you have your docker image!
---

## 3. Open the project in VS Code with Dev Containers and run docker image

1. Install the **Dev Containers** extension in VS Code (`ms-vscode-remote.remote-containers`).
2. Open the project folder in VS Code.
3. Press `F1` (or `Cmd/Ctrl + Shift + P`) or look for "view - command palette"  and type:
```
Dev Containers: Reopen in Container
```
4. VS Code will build (if needed) and start the container defined in `.devcontainer/devcontainer.json`.


---

## 6. Running Python scripts

In the VS Code terminal:
```bash
python main.py
```

Or, for Jupyter notebooks, open a `.ipynb` file and select the .venv kernel.
