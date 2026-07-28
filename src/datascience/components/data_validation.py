import os
from src.datascience import logger
import pandas as pd
from src.datascience.entity.config_entity import DataValidationConfig


class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_columns(self) -> bool:
        try:
            data = pd.read_csv(self.config.unzip_data_dir)
            all_cols = list(data.columns)
            all_schema = set(self.config.all_schema.keys())

            validation_status = all(col in all_schema for col in all_cols)

            with open(self.config.STATUS_FILE, "w", encoding="utf-8") as f:
                f.write(f"Validation Status: {validation_status} \n")

            return validation_status

        except Exception as e:
            raise e

    