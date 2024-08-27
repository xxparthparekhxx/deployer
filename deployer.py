from flask import Flask, request, jsonify
import subprocess
import os
import tarfile
import json

app = Flask(__name__)

# Set a secret token for authorization
SECRET_TOKEN = '<ENTER YOUR TOKEN HERE>'

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stderr

@app.route('/deploy', methods=['POST'])
def deploy():
    token = request.headers.get('Authorization')
    if token != f'Bearer {SECRET_TOKEN}':
        return jsonify({'error': 'Unauthorized'}), 403

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']

    if 'data' not in request.form:
        return jsonify({'error': 'No data part'}), 400
    data = json.loads(request.form['data'])

    commands = data.get('commands', [])
    destination = data.get('destination')

    if not commands or not destination:
        return jsonify({'error': 'Missing commands or destination'}), 400

    # Save and extract the tar file
    tar_path = '/tmp/dist.tar.gz'
    file.save(tar_path)

    with tarfile.open(tar_path, 'r:gz') as tar:
        tar.extractall(path=destination)

    os.remove(tar_path)

    # Change to the destination directory
    os.chdir(destination)

    # Run the provided commands
    results = [run_command(cmd) for cmd in commands]

    return jsonify({'results': results})

@app.route('/command', methods=['POST'])
def command():
    token = request.headers.get('Authorization')
    if token != f'Bearer {SECRET_TOKEN}':
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.json
    commands = data.get('commands', [])

    if not commands:
        return jsonify({'error': 'No commands provided'}), 400

    results = [run_command(cmd) for cmd in commands]
    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
