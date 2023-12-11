import os
from pathlib import Path
import logging


# Setting up logging
logging.basicConfig(level=logging.INFO, format="[%(asctime)s]: %(message)s:")

# Embedded content of exception.py, logger.py and Dockerfile
EXCEPTION_CONTENT = 'import sys\n\n\n# ________________ DEF THE ERROR MESSAGE ________________ #\ndef error_message_detail(error, error_detail: sys):\n    """\n    This function is to return a message regarding error details occuring in the execution of the code\n\n    """\n\n    # no interest in the 1st and 2nd items in the return of the exc_info()\n    _, _, exc_tb = error_detail.exc_info()\n\n    file_name = exc_tb.tb_frame.f_code.co_filename\n    error_message = "Error occured in the script, name: [{0}], line number: [{1}] error message: [{2}]".format(\n        file_name, exc_tb.tb_lineno, str(error)\n    )\n\n    return error_message\n\n\n# ________________ MAKE ERROR CAPTURE HANDLER ________________ #\nclass CustomException(Exception):\n    def __init__(self, error_message, error_detail: sys):\n        super().__init__(error_message)\n        self.error_message = error_message_detail(\n            error_message, error_detail=error_detail\n        )\n\n    def __str__(self):\n        return self.error_message\n'

LOGGER_CONTENT = 'import logging, os\nfrom datetime import datetime\n\nLOG_FILE = f"{datetime.now().strftime(\'%m _%d_%Y_%H_%M_%S\')}.log"\nlogs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)\nos.makedirs(logs_path, exist_ok=True)  # keep on appending the file\n\nLOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)\n\nlogging.basicConfig(\n    filename=LOG_FILE_PATH,\n    # recommended format\n    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",\n    level=logging.INFO,\n)\n'

DOCKERFILE_CONTENT = """\
FROM python:3.9.18
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
"""


project_name = "Mitochondria_segmentation"

# List of files and directories
list_of_files = [
    f"{project_name}",
    f"{project_name}/data",
    f"{project_name}/models",
    f"{project_name}/make_prediction.py",
    f"{project_name}/data_ingestion.py",
    "static",
    "static/images_input",
    "static/images_test",
    "static/js",
    "static/styles",
    "templates",
    "templates/base.html",
    "templates/index.html",
    "templates/documentation.html",
    "app.py",
    "logger.py",
    "exception.py",
    "utils.py",
    "requirements.txt",
    "heroku_common.txt",
    "Dockerfile",
]

for file_path in list_of_files:
    path_obj = Path(file_path)

    if path_obj.is_dir() or (
        path_obj.name not in ["Dockerfile"] and "." not in path_obj.name
    ):
        if not path_obj.exists():
            os.makedirs(path_obj, exist_ok=True)
            logging.info(f"Created directory: {path_obj}")
        else:
            logging.info(f"Directory {path_obj} already exists => re-creating ignored.")
    else:
        if not path_obj.parent.exists():
            os.makedirs(path_obj.parent, exist_ok=True)
            logging.info(f"Created directory for the file: {path_obj.parent}")

        if not path_obj.exists() or path_obj.stat().st_size == 0:
            with open(path_obj, "w") as f:
                if path_obj.name == "exception.py":
                    f.write(EXCEPTION_CONTENT)
                elif path_obj.name == "logger.py":
                    f.write(LOGGER_CONTENT)
                elif path_obj.name == "Dockerfile":
                    f.write(DOCKERFILE_CONTENT)

            logging.info(f"Created file: {path_obj}")

        # Else, just create an empty file
        else:
            logging.info(
                f"File {path_obj} already exists and is not empty => re-creating ignored."
            )

if __name__ == "__main__":
    print("Project structure generated successfully!")
