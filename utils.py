import os, sys, re
from pathlib import Path
from exception import CustomException


# ________________ GET NUMBER OF CLASSES FROM METADATA ________________ #
def get_num_classes(metadata_string: str) -> int:
    """
    Extracts the thing_classes from the metadata string and returns the number of classes.

    Parameters:
    - metadata_string: Metadata in string format

    return:
    - num_classes: Number of classes that will go into the detectron2 model

    """

    try:
        # Extract the substring for thing_classes using regular expressions
        thing_classes_match = re.search(r"thing_classes=\[([^\]]+)\]", metadata_string)

        if thing_classes_match:
            thing_classes_str = thing_classes_match.group(1)
            # Convert the substring to a list of classes
            thing_classes = [x.strip().strip("'") for x in thing_classes_str.split(",")]
            return len(thing_classes)
        else:
            return 0
    except Exception as e:
        raise CustomException(e, sys)


# ________________ MAKE PATHS ________________ #
def make_data_path(root_name):
    """
    Constructs and returns the paths for the training, testing, and validation datasets, given a root directory name.

    Parameters:
    - root_name (str): The name of the root directory under which the datasets reside.

    Returns:
    - train_path (pathlib.Path): Path object pointing to the training dataset directory.
    - val_path (pathlib.Path): Path object pointing to the validation dataset directory.
    - test_path (pathlib.Path): Path object pointing to the testing dataset directory.

    """

    try:
        current_path = os.getcwd()

        train_path = Path(
            os.path.join(
                (os.path.dirname(os.path.dirname(current_path))),
                root_name,
                "input",
                "data",
                "train",
            )
        )

        val_path = Path(
            os.path.join(
                (os.path.dirname(os.path.dirname(current_path))),
                root_name,
                "input",
                "data",
                "val",
            )
        )

        test_path = Path(
            os.path.join(
                (os.path.dirname(os.path.dirname(current_path))),
                root_name,
                "input",
                "data",
                "test",
            )
        )

        return train_path, val_path, test_path

    except Exception as e:
        raise CustomException(e, sys)
