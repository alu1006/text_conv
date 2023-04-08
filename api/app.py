import os
import zipfile
from datetime import date
from io import BytesIO, StringIO

from flask import Flask, request, send_file, render_template
import opencc
import docx2txt

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    files = request.files.getlist('files')
    converted_files = {}

    for file in files:
        if file.filename.endswith('.docx'):
            text = docx2txt.process(file)
        else:
            text = file.read().decode('utf-8', 'ignore')

        converter = opencc.OpenCC('s2t')
        text = converter.convert(text)

        filename = os.path.splitext(file.filename)[0] + '_convert.txt'

        text_buffer = StringIO()
        text_buffer.write(text)
        text_buffer.seek(0)
        # Convert StringIO to BytesIO
        bytes_buffer = BytesIO(text_buffer.getvalue().encode('utf-8'))

        # Save the file to the in-memory dictionary
        converted_files[filename] = bytes_buffer.getvalue()

    if request.form.get('multiple') or len(converted_files) > 1:
        zip_filename = f'{date.today().strftime("%Y%m%d")}_convert.zip'

        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for filename, file_content in converted_files.items():
                # Add the file to the zip archive using a BytesIO object
                zip_file.writestr(filename, file_content)

        zip_buffer.seek(0)
        return send_file(zip_buffer, download_name=zip_filename, as_attachment=True, mimetype='application/zip')

    else:
        filename, file_content = list(converted_files.items())[0]
        bytes_buffer = BytesIO(file_content)
        return send_file(bytes_buffer, download_name=filename, as_attachment=True, mimetype='text/plain')

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
