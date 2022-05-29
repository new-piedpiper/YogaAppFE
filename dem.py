from distutils.log import debug
from flask import Flask, render_template
from flask_socketio import SocketIO
from PIL import Image
from io import BytesIO
from engne import *
import base64
import re


app=Flask(__name__,template_folder='Templates',static_folder='static')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app,cors_allowed_origins="*")

@app.route('/')
def home():
    return render_template('index.html')

@socketio.on('input image')
def check(input):
    print('image_recieved')
    image_data = re.sub('^data:image/.+;base64,', '', input)
    image = Image.open(BytesIO(base64.b64decode(image_data)))
    image = image.resize((320,240))
    image.save('f1.jpg')
    img_arr=cv2.imread('f1.jpg')
    print(ReturnPose(img_arr))
    image.save('f1.jpg')
if __name__=='__main__':
    socketio.run(app,debug=True)