from pymongo import MongoClient
from decouple import config
from werkzeug.security import generate_password_hash


client = MongoClient(config('MONGO_URI'))
db = client['mohith']
col = db['chat_app']


def encrypt(p):
    hashed_password = generate_password_hash(p)
    return hashed_password

def create_room(data):
    col.insert_one({
        "room_code": data['room_code'],
        "room_password": encrypt(data['room_password']),
        "room_name": data['room_name'] ,
        "host": data['name'],
        "members": [ data['name'] ],
        # "limit" : data['limit'] ,
        "created_at": data['timestamp'],
        "chat_history":[
            {
                "member": data['name'],
                "message": " created the room"
            }
        ]

    })

def add_msg(data):
    col


