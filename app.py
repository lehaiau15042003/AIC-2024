from flask import Flask, request, jsonify, redirect, render_template, url_for, session, flash
from flask_restful import Api, Resource
from flask_cors import CORS, cross_origin
import os
#import tensorflow as tf
#from services.video_service import process_video

'''sess = tf.Session()
graph = tf.get_default_graph()

with sess.as_default():
    with graph.as_default():
        models = load_model("model.h5")''' 

app = Flask(__name__, template_folder='webapp/templates', static_folder='webapp/static')
app.config['SECRET_KEY'] = 'admin'
app.config.from_object('config.Config')
api = Api(app)
CORS(app)

@app.route('/')
def base():
    return render_template("base.html")

@app.route('/login', methods=['GET','POST'])
def login():
    error_message = None
    if request.method == 'POST':
        user_name = request.form.get('name')
        password = request.form.get('password')
        if user_name == "admin" and password == "admin":
            session['user'] = user_name
            return render_template("user.html", name=user_name)
        else:
            error_message = "Invalid username or password"
            return render_template('login.html', error=error_message)
    if "user" in session:
        name = session['user']
        return render_template("user.html", name=name)
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for("login"))
    
@app.route('/user')
def user():
    if "user" in session:
        name = session["user"]
        return render_template('user.html', user=name)
    else:
        return redirect(url_for("login"))
            
@app.route('/logo', methods=['POST'])
@cross_origin(origins="*")
def logo():
    pass

class UploadVideo(Resource):
    def post(self):
        pass
        

'''class ProcessVideo(Resource):
    def post(self):
        data = request.json
        video_path = data.get('file_path')
        if not video_path:
            return jsonify({"error": "No file path provided"})
        result = process_video(video_path)
        return jsonify(result)

api.add_resource(UploadVideo, '/upload')
api.add_resource(ProcessVideo, '/process')'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=6080)