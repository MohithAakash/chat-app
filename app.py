from flask import Flask,redirect,url_for,render_template,request
# from flask.helpers import flash
from flask_socketio import SocketIO, join_room , leave_room
import random

app=Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
active_room_ids = []
active_rooms = []


@app.route('/',methods=['GET','POST'])
def home():
    return render_template('index.html')

@app.route("/create-room")
def create_chat_room():
    return render_template('create-room.html')

@app.route("/join-room")
def join_chat_room():
    return render_template('join-room.html')


@app.route( "/chat" , methods=['GET','POST'] )
def chat():

    if request.method == 'POST':
        action = request.form.get('type')
        print(action)
        if action == "create":
            roomname = request.form.get('room-name')
            username = request.form.get('name')
            room_id  = str(generate_room_id())
            # password = request.form.get('password')
            print(username,roomname,room_id)
        
            if username and roomname and room_id :
                active_rooms.append({ "room_id": room_id, "room_name": roomname, "members": [username]  })
                print(active_rooms)
                return render_template('chat.html' , username = username , room_id = room_id , roomname = roomname )

        elif action == "join" :
            username = request.form.get('name')
            room_id  = request.form.get('room-id').strip()
            # print("room-id====", type(room_id))
            roomname = get_room_name(room_id)
            # password = request.form.get('password')
        
            if room_exists(room_id) and username and roomname :
                members = add_member_to_room(room_id,username)
                if members:
                    return render_template('chat.html' , username = username , room_id = room_id , roomname = roomname , members=members[:-1] )

            # else:
            #     flash("room does not exist!")

    return redirect('/')

    # else:
    #     return redirect('/')

@socketio.on('join_room')
def handle_join_room(data):
    
    # app.logger.info(data)
    join_room(data['room_id'])

    socketio.emit('join_room_announcement' , data , room = data['room_id'])

@socketio.on('leave_room')
def handle_leave_room(data):
    
    app.logger.info(data)
    leave_room(data['room_id'])

    socketio.emit('leave_room_announcement' , data , room = data['room_id'])

 
@socketio.on('send_message')
def handle_send_message(data):

    # app.logger.info(data)

    socketio.emit('receive_message' , data , room = data['room_id'])

def generate_room_id():

    while True:
        room_id = random.randint(100001, 999999)
        if not room_exists(room_id):
            break

    return room_id

def room_exists(room_id):

    for room in active_rooms:
        if room['room_id'] == room_id:
            return True

    return False

def get_room_name(room_id):

    for room in active_rooms:
        if room['room_id'] == room_id:
            return room['room_name']

    return False

def add_member_to_room(room_id,username):

    for room in active_rooms:
        if room['room_id'] == room_id:
            room['members'].append(username)
            print(room['members'])
            return room['members']




if __name__ == '__main__':
    socketio.run( app , debug=True )
    # app.run(port=5000,debug=True)