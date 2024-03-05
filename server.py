from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import uuid
import os

app = Flask(__name__)
CORS(app)

@app.route('/execute', methods=['POST'])
def execute_command():
    data = request.json
    try:
        filename = str(uuid.uuid4()) + '.py'
        with open(filename, 'w') as file:
            file.write(data["code"])

        result = subprocess.check_output(['python', filename], stderr=subprocess.STDOUT)
        os.remove(filename)

        # Return the response data in a JSON format
        return jsonify({'data': result.decode('utf-8')})
    except subprocess.CalledProcessError as e:
        os.remove(filename)
        # Return the error message in a JSON format
        return jsonify({'error': f"Error executing command: {e.output.decode('utf-8')}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
