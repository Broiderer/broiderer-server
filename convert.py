import subprocess

def pes_to_svg(input_path, output_path):
    subprocess.run([
        'vpype', 'eread', input_path, 
        'linemerge', 'linesort', 'reloop', 'linesimplify',
        'write', output_path
    ])

def svg_to_pes(input_path, output_path):
    subprocess.run([
        'vpype', 'read', input_path, 
        'efill', '-d 5px', '-t 0px' 
        'ewrite', output_path
    ])