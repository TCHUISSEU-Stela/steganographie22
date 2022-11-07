from flask import Flask,render_template, request, redirect, url_for
import os,random,shutil
from os.path import join, dirname, realpath

app = Flask(__name__)

# enable debugging mode
app.config["DEBUG"] = True

# Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

@app.route('/')
def index():
    # Set The upload HTML template '\templates\index.html'
    return render_template('index.html')

def img_aleatoire():
    random_file=random.choice(os.listdir("static/bank/"))
    return random_file

def entension(fichier):
    split_tup = os.path.splitext(fichier)
    return split_tup

def cache(fichier):
    info=entension(fichier)
    img=img_aleatoire()
    shutil.copyfile('static/bank/'+img, 'static/files/'+img)
    with open('static/files/'+img,'ab') as f, app.open_resource('static/files/'+fichier,'rb') as e:
         f.write(e.read())

    os.rename('static/files/'+img,'static/files/'+info[1]+'_'+img)
    return info[1]+'_'+img
    #dirs=os.listdir("static/files/")
    # for file in dirs:
    #     print(file)


# Get the uploaded files
@app.route("/", methods=['POST'])
def uploadFiles():
      # get the uploaded file
      uploaded_file = request.files['file']
      if uploaded_file.filename != '':
           file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
          # set the file path
           uploaded_file.save(file_path)
           fichier=uploaded_file.filename
           nom_fichier=cache(fichier)
           full_filename = os.path.join(app.config['UPLOAD_FOLDER'], nom_fichier)
           #return redirect(url_for('download'), file = nom_fichier)
           return render_template("download.html",fichier=full_filename,nom_fichier=nom_fichier)

           
          # save the file
      return redirect(url_for('index'))

@app.route('/decrypt/')
def decrypt():
    # Set The upload HTML template '\templates\index.html'
    return render_template('decrypt.html')

def lire_extension(fich):
    #en inverse
    return format(fich.split('_')[0])

def retrouve(fichier):
    ext=lire_extension(fichier)
    with app.open_resource('static/files/'+fichier,'rb') as f:
        content=f.read()
        offset=content.index(bytes.fromhex('FFD9'))
        f.seek(offset + 2)
        with open('static/file/'+'recovery'+ext,'wb') as e:
            e.write(f.read())

    return 'recovery'+ext  


# Get the uploaded files
@app.route("/decrypt/", methods=['POST'])

def uploadFiless():
      # get the uploaded file
      uploaded_file = request.files['file']
      if uploaded_file.filename != '':
           file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
          # set the file path
           uploaded_file.save(file_path)
           fichier=uploaded_file.filename
           nom_fichier = retrouve(fichier) 
           full_filename = os.path.join('static/file', nom_fichier)
           return render_template("download.html",fichier=full_filename,nom_fichier=nom_fichier)
           
          # save the file
      return redirect(url_for('decrypt'))

@app.route('/download/')
def download():
    # Set The upload HTML template '\templates\index.html'
    return render_template('download.html')

if __name__ == "__main__":
    app.run()