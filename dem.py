from flask import Flask, render_template
from flask_socketio import SocketIO

app=Flask(__name__,template_folder='Templates',static_folder='static')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app,cors_allowed_origins="*")

@app.route('/')
def home():
    return render_template('index.html')

@socketio.on('input image')
def check(input):
    print('image_recieved')

if __name__=='__main__':
    socketio.run(app)