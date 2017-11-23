from flask import Flask, json, request, render_template, redirect, url_for
import os, string
app = Flask(__name__)

UPLOAD_FOLDER = 'temp'
ALLOWED_EXTENSIONS = set(['txt'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def main():
    return "Welcome!"

@app.route("/finance_extractor")
def render_view():
    try:
        os.remove('input')
        os.remove('out')
        os.remove('out_to_process')
        os.remove('out.json')
    except OSError as e:
        print(e)
        pass
    return render_template('forms.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    f = request.files['file']
    f.save('input')
    return redirect(url_for('render_result'))

@app.route('/result')
def render_result():
    return render_template('result.html')

@app.route('/extract')
def extract_info():
    import generator
    import chunkner
    import process
    result = json.loads(open('out.json').read())
    who = ", ".join(result['who'])
    when = ", ".join(result['when'])
    howmuch = ", ".join(result['howmuch'])
    why = ", ".join(result['why'])
    return render_template('content.html', who=who, when=when, howmuch=howmuch, why=why)

if __name__ == "__main__":
    app.run()
