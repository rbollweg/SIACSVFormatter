__author__ = 'The Gibs'

import urllib.request
import os
import csv
import re

from flask import render_template, flash, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename

from CSVapp import app

from dateutil import parser

# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = 'csv'
app.config['UPLOAD_FOLDER'] = 'C:/uploads/'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):

        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], "csv_edit.csv")
        file_output_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        reader = open(file_path, "rt", encoding="utf8")
        writer = open(file_output_path, "wt", newline='', encoding="utf8")

        csv_file = csv.reader(reader)
        csv_output = csv.writer(writer)
        for row in csv_file:
            fixed_date = re.search("(\d{1,2}/\d{1,2}/\d{4}\s\d{1,2}:\d{1,2})", row[21])
            row[21] = fixed_date.group(1)
            csv_output.writerow(row)

        reader.close()
        writer.close()
        return redirect(url_for('uploaded_file',
                                filename=filename))
    else:
        return render_template('index.html', error = "incorrect filetype")


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
