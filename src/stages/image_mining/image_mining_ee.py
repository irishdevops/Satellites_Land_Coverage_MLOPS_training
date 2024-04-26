import time
import ee
import pandas as pd

class EE_Requests:

    def __init__(self):
        self.count_iter = 0
        self.count_error = 0
        self.list_error = []
        self.count_success = 0
        self.list_success = []

    def get_execution_summary(self):
        return {
            'count_iter': self.count_iter,
            'count_error': self.count_error,
            'list_error': self.list_error,
            'count_success': self.count_success,
            'list_success': self.list_success
        }

    ##EE_Gabriel_Request_Copernicus(Correct dataset as variable,Number of rows as number,Number 0 no harmonized/Number 1 harmonized)

    ## collection_name: 'COPERNICUS/S2', 'COPERNICUS/S2_SR_HARMONIZED'.
    # Load Sentinel-2 image collection LINK https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2
    # Load Sentinel-2 image collection Harmonized LINK https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED

    def Init_EE_Request(self,data,collection_name: str, older_date: str, newer_date: str, folder_id: str, buffer:int):

        """""""""
        
        Init_EE_Request extract images from COPERNICUS into collection.

        data: pd dataframe 
        collection_name: 'COPERNIC US/S2', 'COPERNICUS/S2_SR_HARMONIZED' + more available at ee collection page (search fro API collection name)
        older_date: older date to search for images "YYYY-MM-dd"
        newer_date: newest to search for images "YYYY-MM-dd"
        folder_id: identifier. must be unique for each run so it doesn't confuse drive folders. "Model2_Zone1" for example.
        buffer: total distance in meters of one side of the square image.

        returns google drive images and execution summarization with number of error and error name list. 
        takes into account to get the first newest image for each request.

        """""""""
        start_time = time.time()

        try:
            query = data
            for index, row in query.iterrows():
                self.count_iter += 1
                print("Iteration number: ", self.count_iter)

                try:
                    self._extract_images(row, collection_name, older_date, newer_date, folder_id, buffer)
                    self.count_success += 1
                    self.list_success.append(row['Image_Name'])
                except Exception as e:
                    print(f"Error: {e}")
                    self.count_error += 1
                    self.list_error.append(row['Image_Name'])

        except KeyboardInterrupt:
            pass  # Handle the KeyboardInterrupt here

        finally:
            end_time = time.time()
            execution_time = end_time - start_time

            summary = self.get_execution_summary()
            summary['execution_time'] = execution_time / 60

            return summary

    def _extract_images(self,row,collection_name: str, older_date: str, newer_date: str, folder_id: str, buffer: int):

        lat = row['lat']
        long = row['long']
        filename= row['Image_Name'] 


        ##NOTE Past Technique: polygon = ee.Geometry.Rectangle([40.024752, -3.593701, 40.048571, -3.570920])##Rectangle( [37.23, 11.66, 37.39, 11.82])#polygon = ee.Geometry.Polygon([[v1_x, v1_y], [v2_x, v2_y], [v3_x, v3_y], [v4_x, v4_y]])
        
        # Create a geometry from the coordinates
        polygon = ee.Geometry.Point(long,lat).buffer(buffer)
        

            # Get the image collection based on the collection ID
            #NOTE Past Technique: image = ee.Image(image_collection_id).select(['SR_B1', 'SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'])#.filterBounds(polygon)##image = ee.Image(image_collection_id).select('B8','B7','B6','B5','B4','B3','B2','B1') 
            
        sentinel2 = ee.ImageCollection(collection_name)
        image = sentinel2.filterDate(older_date, newer_date) \
                .filterBounds(polygon) \
                .filterMetadata('CLOUD_COVERAGE_ASSESSMENT', 'less_than', 1) \
                .select(['B8','B4', 'B3', 'B2']) \
                .first()
        

        
        # Filter, select bands, and get the first image

            # Define the export parameters
        export_params = {
            'image': image,
            'description': filename,
            'folder': (folder_id + "_" + row['CVB1']), # Specify the folder in your Google Drive where you want to save the exported image. If is not created. Will create one
            'fileNamePrefix': filename,
            'scale': 1,  # Adjust the scale according to your needs
            'maxPixels': 999999, ## The scale surpases by far 10m. So is going to pull a good aproximation of pixel from here. That's why we need to set the limit to EE limit per request.
            'region': polygon.getInfo()['coordinates'],  # Adjust the CRS according to your needs
            
        }
        
            # Export the image to Google Drive
        task = ee.batch.Export.image.toDrive(**export_params)
        task.start()
        start_time = time.time()
        while task.status()['state'] in ['READY', 'RUNNING']:
            time.sleep(5)
        

        # # Check if the export completed successfully
        if task.status()['state'] == 'COMPLETED':
            print ("Completed: " + row['Image_Name'] )
            end_time = time.time()
            execution_time = end_time - start_time
            print("Execution time completion: ", execution_time/60, "min")

        else:
            print('Export waiting. Reason '+ task.status()['state'])
            print(task.status().get('error_message', 'No error message available'))
            end_time = time.time()
            execution_time = end_time - start_time
            print("Execution time failure: ", execution_time/60, "min")
