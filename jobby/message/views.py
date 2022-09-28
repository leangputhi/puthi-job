from flask import render_template, Blueprint, request, jsonify, flash, redirect, url_for, abort
from flask_login import current_user, login_required
from jobby.models import Users, Messages, Bids, Offers
from jobby import db, last_updated
from sqlalchemy import or_, and_
from datetime import datetime
from flask_socketio import emit
from .. import socketio

message = Blueprint('message',__name__)

@message.route('/get-message/<type_id>')
@login_required
def getMessage(type_id):
    itemType, itemId = type_id.split('_')
    if itemType == 'b':
        data = Bids.query.filter_by(id=itemId).first_or_404()
        if current_user == data.bidder or current_user == data.bidded.poster:
            return jsonify({"message": data.message})
    elif itemType == 'o':
        data = Offers.query.filter_by(id=itemId, offered=current_user).first_or_404()
        return jsonify({"message": data.message})
    else:
        jsonify({"message": 'Some thing went wrong'})

@message.route('/get-recipient/<int:recipient_id>')
@login_required
def getRecipient(recipient_id):
    user = Users.query.filter_by(id=recipient_id).first_or_404()
    return jsonify({"username": user.name})

@socketio.on('send message')
def handle_message(data):
    recipient_id = data['to']
    body = data['body']
    recipient = Users.query.filter_by(id=recipient_id).first()
    msg = Messages(body=body, recipient=recipient, sender=current_user)
    db.session.add(msg)
    db.session.commit()
    emit("message success", {'success': True})

@socketio.on('connect')
def handle_connection():
    current_user.message_sid = request.sid
    db.session.commit()

# @socketio.on('start writing')
# def handle_writing(data):
#     print("writing event fired")
#     recipient_id = data['recipient_id']
#     recipient = Users.query.filter_by(id=recipient_id).first()
#     print("recipient_id ", recipient_id)
#     emit("put writing field", {'sender_id': current_user.id, 'recipient_id': recipient_id}, room=recipient.message_sid)

@socketio.on('private message')
def handle_private_message(data):
    recipient_id = data['recipient']
    recipient = Users.query.filter_by(id=recipient_id).first()
    private_msg = data['msg']
    new_message = Messages(body=private_msg, recipient=recipient, sender=current_user)
    db.session.add(new_message)
    db.session.commit()
    emit('message sent back', {"prv": private_msg, "sender_id": current_user.id}, room=recipient.message_sid)

@message.route('/get-all-message/<int:person_id>')
@login_required
def handle_all_messages(person_id):
    recipient = Users.query.get(person_id)
    msgs = db.session.query(Messages.body, Messages.timestamp, Messages.sender_id, Messages.recipient_id).filter(or_(and_(Messages.sender_id==current_user.id,
        Messages.recipient_id==person_id),
        and_(Messages.sender_id==person_id, Messages.recipient_id==current_user.id))).all()

    return jsonify({'payload': msgs, 'currentUserId': current_user.id, "recipient_name": recipient.name+" "+recipient.surname, "imgSrcSender": current_user.profile_picture, "imgSrcReciever": recipient.profile_picture})

def get_users(f):
    users = []
    for i in f:
        user = Users.query.get(i)
        users.append(user)
    return users

@message.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    db.session.commit()
    as_a_recipient = db.session.query(Messages.sender_id).filter(Messages.recipient_id==current_user.id).distinct().all()
    as_a_sender = db.session.query(Messages.recipient_id).filter(Messages.sender_id==current_user.id).distinct().all()

    return render_template('message/messages.html',c=get_users(set(as_a_recipient+as_a_sender)), last_updated=last_updated)
