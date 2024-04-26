import os
import numpy as np
import rasterio
from PIL import Image

class TransformGeoTIFtoJPEG:
    def __init__(self):
        pass

    def runfolder_transform(self, targetfolder, outputfolder):
        for subfolder_name in os.listdir(targetfolder):
            if subfolder_name.startswith("."):
                continue

            # Convert TIFF to JPEG using OpenCV
            tif_folder = os.path.join(targetfolder, subfolder_name)
            jpeg_folder = os.path.join(outputfolder, subfolder_name)

            os.makedirs(jpeg_folder, exist_ok=True)
            counter = 0

            for tif_file in os.listdir(tif_folder):
                counter += 1
                file_path = os.path.join(tif_folder, tif_file)

                if tif_file.endswith(".tif"):
                    self.transform_GeoTIFtoJPG(file_path, jpeg_folder)

            print(f"Transformation saved as JPEG: {tif_folder}")

    def transform_GeoTIFtoJPG(self, image, upload_path):
        input_geotiff_path = image
        output_jpeg_path = upload_path

        with rasterio.open(input_geotiff_path) as src:
            red_band = src.read(1).astype(np.uint8)
            IRR_band = src.read(4).astype(np.uint8)
            blue_band = src.read(3).astype(np.uint8)
            green_band = src.read(2).astype(np.uint8)

        ir_band_min = IRR_band.min()
        ir_band_max = IRR_band.max()
        normalized_IRR_band = ((IRR_band - ir_band_min) / (ir_band_max - ir_band_min) * 255).astype('uint8')

        g_band_min = green_band.min()
        g_band_max = green_band.max()
        normalized_green_band = ((green_band - g_band_min) / (g_band_max - g_band_min) * 180).astype('uint8')

        b_band_min = blue_band.min()
        b_band_max = blue_band.max()
        normalized_blue_band = ((blue_band - b_band_min) / (b_band_max - b_band_min) * 180).astype('uint8')

        r_band_min = red_band.min()
        r_band_max = red_band.max()
        normalized_red_band = ((red_band - r_band_min) / (r_band_max - r_band_min) * 180).astype('uint8')

        color_image = np.stack((normalized_IRR_band,normalized_blue_band,normalized_green_band), axis=-1)
        pil_image = Image.fromarray(color_image)

        output_jpeg_path = os.path.join(output_jpeg_path, input_geotiff_path.replace(".tif", "").rsplit('/', 1)[-1] + ".JPEG")
        pil_image.save(output_jpeg_path, format='JPEG')

        print(f"Color image saved as JPEG: {output_jpeg_path}")
