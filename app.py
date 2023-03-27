import subprocess
from flask import Flask, request, send_file, render_template, jsonify
import time
from flask_cors import CORS
import os
import edge_tts

app = Flask(__name__)
CORS(app)

# 自定义异常处理函数


@app.errorhandler(ValueError)
def handle_value_error(error):
    response = jsonify({"error": str(error)})
    response.status_code = 400
    return response


@app.route('/', methods=['GET'])
def tts():
    return render_template('edge-tts.html')


@app.route('/submit', methods=['POST'])
def run_command():
    text = request.form['text']
    voice = request.form['voice']
    rate = request.form['rate']

    tts_arr = []
    text = ''
    tts_arr.append('/usr/local/bin/edge-tts')
    # text voice rate file_upload
    if 'text' in request.form:
        text = request.form.get('text')
    if 'voice' in request.form:
        voice = request.form.get('voice')
        tts_arr.append('--voice')
        tts_arr.append(voice)
    if 'rate' in request.form:
        rate = request.form.get('rate')
        tts_arr.append('--rate')
        tts_arr.append(rate)
    if 'file_upload' in request.files:
        file = request.files.get('file_upload')
        if file.filename.endswith('.txt'):
            text = file.read().decode('utf-8')

    if len(text) > 0:
        tts_arr.append('--text')
        tts_arr.append(text)
    else:
        raise ValueError('请输入待合成文本或者上传txt文件')

    tts_arr.append('--write-media')
    mp3_name = str(time.strftime('%Y-%m-%d_%H-%M-%S'))+'.mp3'
    tts_arr.append(mp3_name)

    output = subprocess.check_output(tts_arr)

    response = send_file(mp3_name, mimetype='audio/mpeg')

    os.remove(os.path.abspath(mp3_name))

    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2233)
