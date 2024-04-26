import os
from unidecode import unidecode
import pandas as pd

class DataLoader:
    def __init__(self, coordinates_filename):

        self.coordinates_filename = coordinates_filename

    def _construct_full_path(self,coordinates_filename):
            # Get the current script's directory
            data_directory = "datasets/coordinates/"
            
            # Get the current working directory
            current_path = os.getcwd()

            # Extract the project path from the current working directory
            project_path = os.path.dirname(current_path)

            # Construct the full path
            return os.path.join(project_path,data_directory, coordinates_filename)

    def read_csv(self):
        # Read the CSV file using pandas and automatically assign headers as column names
        path = self._construct_full_path(self.coordinates_filename)
        df = pd.read_csv(path)
        return df

class PreprocessClasses:
    def __init__(self, levels_to_keep, n_images_byclass):
        self.levels_to_keep = levels_to_keep
        self.n_images_class = n_images_byclass


    def clean_and_filter(self,df):

        original = df.copy() 

        def replace_if_contains(text):
            for level in self.levels_to_keep:
                if text in level:
                    return level
            return text
            
        def get_first_rows(group):
            return group.head(self.n_images_class)

        # Apply the custom function to the 'CVB1' column
        df['CVB1'] = df['CVB1'].apply(replace_if_contains)

        # Reset the index if needed
        df = df.reset_index(drop=True)

        # Group by 'CVB1' and apply the custom function to each group
        df = df.groupby('CVB1', group_keys=False).apply(get_first_rows)

        # Reset the index if needed
        df = df.reset_index(drop=True)

        self._display_info(original,df)

        return df

    def _display_info(self,original,df):
        
        # Display information about the cleaned DataFrame
        print("Number of ORIGINAL unique levels in the 'CVB1':", original['CVB1'].nunique())
        print("Number of CURRENT unique levels in the 'CVB1':", df['CVB1'].nunique())

        unique_values = df['CVB1'].unique()
        unique_values_list = unique_values.tolist()

        or_unique_values = original['CVB1'].unique()
        or_unique_values_list = or_unique_values.tolist()

        # Display unique values
        print("Unique original values in the 'CVB1':", or_unique_values_list)

        print("Unique current values in the 'CVB1':", unique_values_list)


class ImageNameProcessor:
    def __init__(self):
        pass

    def process_image_names(self,df):

        # Concatenate columns to create 'Image_Name'
        df['Image_Name'] = (df['fid'].astype(str) + ':' + df['CVB1'])
        
        # Replace spaces with underscores and '+' with '-'
        df['Image_Name'] = df['Image_Name'].replace(r'\s+', '_', regex=True).replace(r'\+', '-', regex=True)
        
        # Apply unidecode to remove accents
        df['Image_Name'] = df['Image_Name'].apply(unidecode)
        
        # Calculate the length of 'Image_Name' for testing (using the first row)
        df['Image_Name_Length'] = len(df['Image_Name'][0])

        # Sort the DataFrame by 'CVB1' column in descending order
        df = df.sort_values(by='CVB1', ascending=False)

        # Reset the index after sorting
        df = df.reset_index(drop=True)

        return df