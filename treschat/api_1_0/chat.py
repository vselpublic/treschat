from flask import jsonify, request, g, abort, url_for, current_app
from . import api
from ..dao import Message
from ..model import insert_to_db

@api.route('/chat/add_message', methods=['POST'])
def add_new_message_from_json():
    #print request.json
    message = Message.from_json(request.json)
    if g.current_user.id == message["userid"]:
        insert_to_db(message)
    return jsonify(message.to_json())

@api.route('/chat/get_all', methods=['GET'])
#ALL Messages for 1 chat
def get_all_messages():
    pass

@api.route('/chat/leave', methods=['GET'])
#leave chat
def leave_chat():
    pass