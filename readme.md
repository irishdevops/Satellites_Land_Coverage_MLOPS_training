This repo contains customized functions that allow you to train models for satellital imagery by data mining images from earth engine. The user needs a query with layer coordinates.

### **Instructions**

1 - follow the notebooks instructions, which manage different stages.First notebook is used for data mining. <br>

2 - Second notebook is used for training the models from a .jpeg collection. Therefore, both notebooks are indepdendant and can be used separately. <br>
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