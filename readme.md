This repo contains customized functions that allow you to train models for satellital imagery data mining from earth engine. The user needs a query with the coordinates to obtain images from. The user can define the resolution and area size to obtain.
### **Instructions**
1 - clone repo from git <br>
2 - follow the notebooks instructions, which manage different stages.First notebook is used for data mining. Second notebook is used for training the models from a .jpeg collection. Therefore, both notebooks are indepdendant and can be used separately. <br>
Note: You will need to have an active earth engine account and an active project to connect for the data mining process. https://earthengine.google.com/

### **Pending work:**

- Automation of the OS for model training notebook. OS has to be manually set up by URL by users for each of the process outputs (model logs, missclassified samples, model metadata, stats...).
- Commenting of the functions and explanation on Earth Engine can be improved. Following repo is recommended as a complementay source: https://github.com/google/earthengine-api

### **Advantages and unique value:**

- Process of data mining + training models just following notebook 1 and notebook 2 instructions is unique to this computer vision experiment. you can choose the pre-trained models from tensorflow and pytorch that have been selected or use your own models.
