from flask import Flask, request, jsonify, send_from_directory, redirect, render_template, session, url_for, render_template_string
from flask_restful import Api, Resource
import os
#from services.video_service import process_video

app = Flask(__name__, template_folder='webapp/templates', static_folder='webapp/static')
app.config.from_object('config.Config')
api = Api(app)


@app.route('/')
def base():
    return render_template("base.html")

'''@app.route('/')
def user():
    if "user" in session:
        name = session['user']
    else:
        return redirect'''

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['name']
        if user_name:
            session['user'] = user_name
            return redirect(url_for("user", name=user_name))
    if "user" in session:
        name = session['user']
    return render_template('login.html')

@app.route('/')
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
    app.run(debug=True)