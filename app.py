from flask import Flask, json, request, render_template
import os
app = Flask(__name__)

UPLOAD_FOLDER = 'temp'
ALLOWED_EXTENSIONS = set(['txt'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def main():
    return "Welcome!"

@app.route("/finance_extractor")
def render_view():
    # os.remove('input')
    # os.remove('out')
    # os.remove('out_to_process')
    return render_template('forms.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    f = request.files['file']
    f.save('input')
    import generator
    import chunkner
    import process
    return 'file uploaded successfully'

# @app.route('/result')
# def render_result():


if __name__ == "__main__":
    app.run()
