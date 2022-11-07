from flask import Flask,render_template, request, redirect, url_for
import os
from os.path import join, dirname, realpath

app = Flask(__name__)

# enable debugging mode
app.config["DEBUG"] = True

# Upload folder
UPLOAD_FOLDER = 'static/file'

app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

@app.route('/decrypt.html')
def decrypt():
    # Set The upload HTML template '\templates\index.html'
    return render_template('decrypt.html')

def retrouve(fichier):
    with app.open_resource('download.jpg','rb') as f:
        content=f.read()
        offset=content.index(bytes.fromhex('FFD9'))
        f.seek(offset + 2)
        with open('flask.pdf','wb') as e:
            e.write(f.read())


# Get the uploaded files
@app.route("/decrypt.html", methods=['POST'])
def uploadFiles():
      # get the uploaded file
      uploaded_file = request.files['file']
      if uploaded_file.filename != '':
           file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
          # set the file path
           uploaded_file.save(file_path)
           fichier=uploaded_file.filename
           retrouve(fichier)
           return f'Filename: {fichier}'
           
          # save the file
      return redirect(url_for('decrypt'))

if __name__ == "__main__":
    app.run()