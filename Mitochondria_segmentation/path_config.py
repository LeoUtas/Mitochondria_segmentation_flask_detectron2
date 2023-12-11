import os, sys


# ________________ HANDLE THE PATH THING ________________ #
# get the absolute path of the script's directory
script_path = os.path.dirname(os.path.abspath(__file__))
# get the parent directory of the script's directory
parent_path = os.path.dirname(script_path)
sys.path.append(parent_path)

from dataclasses import dataclass

# from detectron2.data.datasets import register_coco_instances
# from detectron2.data import MetadataCatalog, DatasetCatalog


@dataclass
class PathConfiguration:
    """
    This class is to handle the path directing to where the images located.

    """

    path_to_images_input: str = os.path.join(
        parent_path, os.path.join("static", "images_input")
    )
    path_to_images_output: str = os.path.join(
        parent_path, os.path.join("static", "images_output")
    )
    path_to_train_JSON: str = os.path.join(
        parent_path,
        os.path.join(
            "Mitochondria_segmentation",
            "data",
            "train",
            "train_images",
            "train.json",
        ),
    )
    path_to_train_images: str = os.path.join(
        parent_path,
        os.path.join(
            "Mitochondria_segmentation",
            "data",
            "train",
            "train_images",
        ),
    )
    path_to_chosen_model_detectron2: str = os.path.join(
        parent_path,
        os.path.join("Mitochondria_segmentation", "models", "chosen_model_detectron2"),
    )
