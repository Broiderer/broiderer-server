import os
from datetime import datetime, timedelta
from flask import Flask, request, redirect, send_from_directory, url_for, abort
from werkzeug.utils import secure_filename
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from convert import pes_to_svg, svg_to_pes

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["*", "https://yourapp.com"]}})
cwd = os.getcwd()
app.config['UPLOAD_FOLDER'] = os.path.join(cwd, 'static/uploads')
app.config['CONVERTED_FOLDER'] = os.path.join(cwd, 'static/converted')
ALLOWED_EXTENSIONS = {'svg', 'pes'}
TIMEOUT = timedelta(hours=1)

def delete_expired_files():
    now = datetime.now()
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
        if now - creation_time > TIMEOUT:
            os.remove(file_path)
    for filename in os.listdir(app.config['CONVERTED_FOLDER']):
        file_path = os.path.join(app.config['CONVERTED_FOLDER'], filename)
        creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
        if now - creation_time > TIMEOUT:
            os.remove(file_path)


# Create and configure the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(delete_expired_files, 'interval', minutes=15)
scheduler.start()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files.get('file')
    extensionFrom = request.args.get('extensionFrom')
    extensionTo = request.args.get('extensionTo')
    if file:
        if allowed_file(file.filename) and extensionFrom and extensionTo:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            converted_filename = os.path.splitext(filename)[0] + '.' + extensionTo
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            output_path = os.path.join(app.config['CONVERTED_FOLDER'], converted_filename)
            
            if extensionTo == 'svg' and extensionFrom == 'pes':
                pes_to_svg(input_path, output_path)
            elif extensionTo == 'pes' and extensionFrom == 'svg':
                svg_to_pes(input_path, output_path)
            else:
                abort(400, 'Invalid file or extension')

            download_url = url_for('download', filename=converted_filename)
            if os.path.isfile(os.path.join(app.config['CONVERTED_FOLDER'], converted_filename)):
                return download_url
            else:
                abort(400, 'File cound not be converted')
        else:
            abort(400, 'Invalid file or extension')
    else:
        abort(400, 'No file provided')
    return ''


@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    return send_from_directory(app.config['CONVERTED_FOLDER'], filename)