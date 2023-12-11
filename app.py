import os, sys

# ________________ HANDLE THE PATH THING ________________ #
# get the absolute path of the script's directory
script_path = os.path.dirname(os.path.abspath(__file__))
# get the parent directory of the script's directory
parent_path = os.path.dirname(script_path)
sys.path.append(parent_path)

from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, flash, url_for
from Mitochondria_segmentation.path_config import *
from Mitochondria_segmentation.make_prediction import *
from exception import CustomException
from time import time
from datetime import datetime

# **** --------- **** #
chosen_model_detectron2 = "COCO-InstanceSegmentation/mask_rcnn_R_101_FPN_3x.yaml"
thresh_score = 0.5
# **** --------- **** #


UPLOAD_FOLDER = os.path.join("static", "images_input")
SECRET_KEY = os.environ.get("SECRET_KEY", "Whatever")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


app = Flask(__name__, static_folder="static")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = SECRET_KEY


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def render_index():
    return render_template("index.html", current_year=datetime.now().year)


@app.route("/detectron2")
def render_detectron2():
    return render_template("detectron2.html", current_year=datetime.now().year)


@app.route("/detectron2", methods=["POST"])
def upload_image_detectron2():
    try:
        if request.method == "POST":
            if "image" not in request.files:
                flash("There is no file")
                return redirect(request.url)

            image = request.files["image"]

            if image.filename == "":
                flash("No image uploaded")
                return redirect(request.url)

            if not allowed_file(image.filename):
                flash(
                    "Invalid file type. Please upload an image (i.e., JPG, JPEG, PNG)."
                )
                return redirect(request.url)

            elif image:
                start_time = time()

                image_file_name = secure_filename(image.filename)
                image_file_ext = os.path.splitext(image_file_name)[1]

                full_path_to_uploaded_image = os.path.join(
                    app.config["UPLOAD_FOLDER"], image_file_name
                )

                image.save(full_path_to_uploaded_image)

                ModelConfigurator = Detectron2Configuration(
                    chosen_model_detectron2, thresh_score
                )
                predictor, metadata = ModelConfigurator.make_configuration()

                MitoSegmentator = Detectron2Segmentation(predictor, metadata)
                (
                    total_objects,
                    mean_area,
                    image_id,
                    csv_file_name,
                ) = MitoSegmentator.make_prediction()

                execution_time = round(time() - start_time, 2)
                print(csv_file_name)
                print(image_id)

                # flashing messages
                flash(image_id)
                flash(str(total_objects))
                flash(str(round(float(mean_area), 2)))
                flash(csv_file_name)
                flash(str(execution_time))

                return redirect(url_for("render_detectron2"))

    except Exception as e:
        raise CustomException(e, sys)


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html", current_year=datetime.now().year), 500


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", current_year=datetime.now().year), 404


@app.route("/test-images")
def render_test_images():
    image_dir = os.path.join("static", "images_test")
    image_files = [
        file
        for file in os.listdir(image_dir)
        if file.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    image_files.sort()  # ensure files are sorted by name
    return render_template(
        "test_images.html", current_year=datetime.now().year, image_files=image_files
    )


if __name__ == "__main__":
    port = int(
        os.environ.get("PORT", 5000)
    )  # define port so we can map container port to localhost
    app.run(host="0.0.0.0", port=port, debug=False)  # define 0.0.0.0 for Docker
