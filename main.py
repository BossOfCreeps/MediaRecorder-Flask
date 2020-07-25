import json
import base64
import speech_recognition as sr
from os import path
#from pydub import AudioSegment
import subprocess

from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/test", methods=["POST"])
def hello():
    return json.dumps({"len": write_to_file(str(request.form)[59:][:-4].replace(" ", "+").encode())}, ensure_ascii=False)


def write_to_file(base64_audio):
    wav_file = open("temp.wav", "wb")
    decode_string = base64.b64decode(base64_audio)
    wav_file.write(decode_string)
    return recognise()


def recognise(file="temp.wav"):
    subprocess.call("ffmpeg -y -i temp.wav temp2.wav", shell=True)

    r = sr.Recognizer()

    with sr.AudioFile('temp2.wav') as source:
        audio = r.record(source)
    try:
        text = "Text: " + r.recognize_google(audio, language="ru-RU")
    except Exception as e:
        text = "Exception: " + str(e)

    return text


if __name__ == "__main__":
    app.run("0.0.0.0", 5001, debug=True, ssl_context=("full.pem", "priv.pem"))
