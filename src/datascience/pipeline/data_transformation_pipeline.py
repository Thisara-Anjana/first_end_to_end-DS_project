from src.datascience.config.configuration import ConfigurationManager
from src.datascience.components.data_transformation import DataTransformation
from src.datascience import logger

from pathlib import Path


STAGE_NAME = "Data Trnasformation Stage"


class DataTransformationTrainingPipeline:
    def __init__(self):
        pass

    @staticmethod
    def _read_validation_status(status_file: Path | str = "artifacts/data_validation/status.txt") -> bool:
        status_path = Path(status_file)
        if not status_path.exists():
            raise FileNotFoundError(f"Validation status file not found: {status_path}")

        with status_path.open("r", encoding="utf-8") as f:
            content = f.read().strip()

        if "Validation Status:" not in content:
            raise ValueError(f"Unexpected validation status content: {content}")

        status_value = content.split(":", 1)[1].strip().split()[0]
        return status_value.lower() == "true"

    def initiate_data_transformation(self):
        try:
            if self._read_validation_status():
                config = ConfigurationManager()
                data_transformation_config = config.get_data_transformation_config()
                data_transformation = DataTransformation(config=data_transformation_config)
                data_transformation.train_test_spliting()
            else:
                raise Exception("Your data scheme is not valid")

        except Exception as e:
            print(e)
            raise