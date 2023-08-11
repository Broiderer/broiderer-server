import os
from flask import Flask, request, send_from_directory, url_for, abort
from werkzeug.utils import secure_filename
from flask_cors import CORS
from convert import pes_to_svg, svg_to_pes

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://broiderer.com", "https://www.broiderer.com"]}})
cwd = os.getcwd()
app.config['UPLOAD_FOLDER'] = os.path.join(cwd, 'static/uploads')
app.config['CONVERTED_FOLDER'] = os.path.join(cwd, 'static/converted')
ALLOWED_EXTENSIONS = {'svg', 'pes'}
MAX_FILE_SIZE = 0.1 * 1024 * 1024  # 100ko

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def file_size_exceeds_limit(file_path):
   return os.path.getsize(file_path) > MAX_FILE_SIZE

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files.get('file')
    extensionFrom = request.args.get('extensionFrom')
    extensionTo = request.args.get('extensionTo')

    if file:
        if allowed_file(file.filename) and extensionFrom and extensionTo:

            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            if file_size_exceeds_limit(file_path):
                os.remove(file_path)
                abort(400, 'File size exceeds the allowed limit')

            converted_filename = os.path.splitext(filename)[0] + '.' + extensionTo
            app.logger.info('%s', converted_filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            output_path = os.path.join(app.config['CONVERTED_FOLDER'], converted_filename)
            app.logger.info('%s', input_path)
            app.logger.info('%s', output_path)
            if extensionTo == 'svg' and extensionFrom == 'pes':
                pes_to_svg(input_path, output_path)
            elif extensionTo == 'pes' and extensionFrom == 'svg':
                svg_to_pes(input_path, output_path, request.args.get('tolerance'), request.args.get('distance'))
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