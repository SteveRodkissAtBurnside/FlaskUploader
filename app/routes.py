import os
from flask import render_template, request, url_for, redirect, send_from_directory, jsonify
from flask import json
from flask_sqlalchemy import model
from werkzeug.utils import secure_filename
from app import app, db
from app.models import ModelFile


@app.route("/")
def home():
    modelfiles = ModelFile.query.all()
    return render_template("home.html", modelfiles=modelfiles)

@app.route("/uploads", methods=['GET','POST'])
def uploads():
    if request.method == 'POST':
        #we clicked submit
        for uploaded_file in request.files.getlist('file'):
            if uploaded_file.filename != '':
                filename = secure_filename(uploaded_file.filename)
                uploaded_file.save(os.path.join( app.config['UPLOAD_FOLDER'], filename))
                #put it in the database then rediriect
                newfile = ModelFile(filename=filename)
                db.session.add(newfile)
                db.session.commit()
        return redirect(request.url)
    #this is a get
    modelfiles = ModelFile.query.all()
    return render_template('uploads.html', modelfiles=modelfiles)

@app.route('/model/<int:id>', methods=['GET','POST'])
def get_model(id):
    #get a particular model from it's id
    filename = ModelFile.query.filter_by(id=id).first().filename
    return send_from_directory('static/models', filename)
    #return filename

@app.route('/delete', methods=['GET','POST'])
def delete():
    if request.method == 'POST':
        id_to_delete = int(request.form['id'])
        print(f"id: {id_to_delete}")
        item_to_delete = db.session.query(ModelFile).filter(ModelFile.id==id_to_delete).first()
        #maybe delete the file too!!
        modelpath = f"app/static/models/{item_to_delete.filename}"
        print(modelpath)
        os.remove(modelpath)
        db.session.delete(item_to_delete)
        db.session.commit()
    return redirect(request.referrer)        #redirect back to the page you came from

@app.route('/get_all_models')
def get_all_models():
    all_files = ModelFile.query.all()
    result = f'{{"models": {json.dumps(all_files)}\n}}'
    print(result)
    return result