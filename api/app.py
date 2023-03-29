import os
import zipfile
from datetime import date
from io import BytesIO

from flask import Flask, request, send_file, render_template
import opencc
import docx2txt

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['files']

    if file.filename.endswith('.docx'):
        text = docx2txt.process(file)
    else:
        text = file.read().decode('utf-8', 'ignore')

    converter = opencc.OpenCC('s2t')
    text = converter.convert(text)

    filename = os.path.splitext(file.filename)[0] + '_convert.txt'

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)

    if request.form.get('multiple'):
        zip_filename = f'{date.today().strftime("%Y%m%d")}_convert.zip'

        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for filename in os.listdir():
                if filename.endswith('_convert.txt'):
                    zip_file.write(filename)

        zip_buffer.seek(0)
        return send_file(zip_buffer, attachment_filename=zip_filename, as_attachment=True)

    else:
        return send_file(filename, as_attachment=True)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
