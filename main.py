from __future__ import print_function
import os
import cloudmersive_barcode_api_client
from cloudmersive_barcode_api_client.rest import ApiException
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename

API_KEY = "ad54f504-d0f2-48a1-82f4-1d34e89c49ca"
image_path = ""
barcode_data = ""


def get_barcode():
    # Configure API key authorization: Apikey
    configuration = cloudmersive_barcode_api_client.Configuration()
    configuration.api_key['Apikey'] = API_KEY
    # create an instance of the API class
    api_instance = cloudmersive_barcode_api_client.BarcodeScanApi(
        cloudmersive_barcode_api_client.ApiClient(configuration))
    # file | Image file to perform the operation on.  Common file formats such as PNG, JPEG are supported.
    try:
        # Scan and recognize an image of a barcode
        api_response = api_instance.barcode_scan_image(image_path)
    except ApiException as e:
        print("Exception when calling BarcodeScanApi->barcode_scan_image: %s\n" % e)

    return api_response.raw_text


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = "ghijlknmkmlknoihuo78969jokpo["
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def home():
    global image_path, barcode_data
    if request.method == "GET":
        return render_template("index.html")
    else:
        file = request.files['filename']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_path = f"static/uploads/{filename}"
        barcode_data = get_barcode()
        flash(f"{barcode_data}")
        return redirect(url_for("home"))


@app.route("/data")
def data():
    return "<h1>hello</h1>"


if __name__ == "__main__":
    app.run(debug=True)



