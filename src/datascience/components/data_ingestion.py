import os
import urllib.request as request
from src.datascience import logger
import zipfile

from src.datascience.entity.config_entity import (DataIngestionConfig)

##component data ingestion

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config


##download file file

    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            filename, headers = request.urlretrieve(
                url=self.config.source_URL,
                filename=self.config.local_data_file
            )
            print(f"{filename} downloaded! with following info: \n{headers}")
        else:
            print(f"File already exists of size: {round(os.path.getsize(self.config.local_data_file)/1024**2, 2)} MB")

    
    def extract_zip_file(self):
        import zipfile
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)