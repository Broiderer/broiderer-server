import subprocess
from flask import Flask
app = Flask(__name__)
def pes_to_svg(input_path, output_path):
    subprocess.run([
        'vpype', 'eread', input_path,
        'linemerge', 'linesort', 'reloop', 'linesimplify',
        'write', output_path
    ])

def svg_to_pes(input_path, output_path, tolerance, distance):
    app.logger.info(tolerance)
    app.logger.info(distance)
    subprocess.run([
        'vpype', 'read', input_path,
        'efill', '-d', distance if distance else '5px', '-t', tolerance if tolerance else '1px',
        'ewrite', output_path
    ])