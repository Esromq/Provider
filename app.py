from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from datetime import datetime, timedelta
import os
from flask_app.database.db import db, init_db
from flask_app import create_app
#from pydf import generate_pdf
import logging
logging.basicConfig(level=logging.DEBUG)

app = create_app()

from flask_app.models import claims

# Ensure necessary directories exist
DOCUMENTS_DIR = os.path.join(os.getcwd(), "documents")
ENROLLMENT_FORMS_DIR = os.path.join(DOCUMENTS_DIR, "Enrollment Forms")
os.makedirs(ENROLLMENT_FORMS_DIR, exist_ok=True)

    
@app.route('/')
def index():
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    logging.info("Rendering index.html")

    return render_template('index.html')


@app.route('/monthly_claim')
def monthly_claim():
   return render_template()

#@app.route('/download/<filename>', methods=['GET'])
#def download_file(filename):
#    file_path = os.path.join(ENROLLMENT_FORMS_DIR, filename)
#    if os.path.exists(file_path):
#        return send_file(file_path, as_attachment=True)
#    else:
#        return jsonify({"error": "File not found"}), 404



@app.route('/routes', methods=['GET'])
def list_routes():
    import urllib
    return '\n'.join(
        sorted(
            f"{rule.endpoint}: {rule.methods} -> {urllib.parse.unquote(rule.rule)}"
            for rule in app.url_map.iter_rules()
        )
    )
    
@app.before_request
def log_request():
    logging.debug(f"Received {request.method} request for {request.path}")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        return request.get_json()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)


