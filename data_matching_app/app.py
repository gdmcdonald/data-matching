from flask import Flask, request, render_template
import pandas as pd
from data_processing import DataProcessor

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file1 = request.files['file1']
    file2 = request.files['file2']
    columns = request.form.getlist('columns')

    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    processor = DataProcessor(df1, df2, columns)
    exact_match = processor.exact_match()
    substring_match = processor.substring_match()
    fuzzy_match = processor.fuzzy_match()

    results = pd.concat([exact_match, substring_match, fuzzy_match])
    results = results.drop_duplicates()

    return render_template('result.html', columns=columns, results=results.values.tolist())

if __name__ == '__main__':
    app.run(debug=True)
