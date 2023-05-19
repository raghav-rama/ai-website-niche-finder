from flask import Blueprint, render_template, request
import pandas as pd
import time

bp = Blueprint('upload_csv', __name__)

@bp.route('/upload_csv', methods=['POST'])
def upload_csv():
    csv_file = request.files['csv_file']
    df = pd.read_csv(csv_file)
    time.sleep(5)
    print(df)
    # Do something with the CSV data, e.g. process it or save it to a database
    return 'CSV file uploaded successfully'
