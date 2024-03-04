from Video_Processor import Vid2Sum, translate
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from os import path
import requests

app = Flask(__name__)
CORS(app)
app.debug = True

@app.route("/")
def index():
    return render_template("webSite.html")

UPLOAD_FOLDER = path.join(app.root_path, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
@app.route("/process_video", methods=["POST"])
def process_video():
    if request.method == "POST":
        try:
            video_file = request.files["video"]
            filename = "uploaded_video.mp4" 
            file_path = path.join(app.config['UPLOAD_FOLDER'], filename)
            video_file.save(filePath)

            input_lang = request.form["inputLang"]
            output_lang = request.form["outputLang"]

            result = Vid2Sum(filePath)

            if output_lang.lower() != "english":
                translated_text = translate(result, "en", output_lang)
                if translated_text:
                    result = translated_text
                    return result

            response = app.response_class(
                response=result,
                status=200,
                headers={
                    "Access-Control-Allow-Origin": "*"
                },
            )

            return response

        except KeyError as e:
            # If 'text' key is not found in the response
            return jsonify(error="Text not found in the response from audio-to-text model", original_error=str(e)), 500

        except Exception as e:
            # Catch any other exceptions and return an informative error message
            return jsonify(error=str(e)), 500
    else:
        return "wrong method sent"
