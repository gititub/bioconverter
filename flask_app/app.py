from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_type = request.form.get('input')
        output_type = request.form.get('output')
        input_text = request.form.get('text')

        # Process the input_type, output_type, and input_text
        # Run the Python script using subprocess
        command = f'python ptc_extract_pmids.py {input_type} {output_type} "{input_text}"'
        subprocess.run(command, shell=True)

        return render_template('index.html', message='Script executed successfully!')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
