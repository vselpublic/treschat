from flask import render_template, redirect, url_for, flash, request
from flask.ext.login import login_required, current_user
from . import main
from ..dao import User, Chat, Message
from ..model import insert_to_db
from .forms import AddChatForm, AddMessageForm, LeaveChatForm


@main.route('/')
def index_html():
    #current_app.logger.error('An error occurred')
   return redirect(url_for('auth.login'))

@main.route('/show_chats', methods=['GET', 'POST'])
@login_required
def show_chats():
    chats = Chat.query.all()
    form = AddChatForm()
    if form.validate_on_submit():
        chat = Chat(chatname = form.chatname.data)
        chat.chat_partisipants.append(current_user)
        print chat.chat_partisipants
        insert_to_db(chat)
        flash('The chat has been updated.')
        return redirect(url_for('main.show_chats',username = current_user.username))
    return render_template('chats.html', chats = chats, current_user = current_user, form = form)


@main.route('/show_chats/<username>', methods=['GET', 'POST'])
@login_required
def show_my_chats(username):
    if username != current_user.username:
       return redirect(url_for('main.show_my_chats',username = current_user.username))
    chats = Chat.query.filter(Chat.chat_partisipants.any(username=username)).all()
    form = AddChatForm()
    if form.validate_on_submit():
        chat = Chat(chatname = form.chatname.data)
        chat.chat_partisipants.append(current_user)
        print chat.chat_partisipants
        insert_to_db(chat)
        flash('The chat has been updated.')
        return redirect(url_for('main.show_chats',username = current_user.username))
    return render_template('chats.html', chats = chats, current_user = current_user, form = form)


@main.route('/search_for_chat/', methods=['POST'])
@login_required
def search_for_chat():
    search_text = request.form['search_text']
    chats = Chat.query.filter(Chat.chatname.like("%"+search_text+"%")).all()
    form = AddChatForm()
    return render_template('chats.html', chats = chats, current_user = current_user, form = form)


@main.route('/chat/<int:id>', methods=['GET', 'POST'])
@login_required
def show_chat(id):
    chat = Chat.query.filter_by(id = id).first()
    if current_user not in chat.chat_partisipants:
        chat.chat_partisipants.append(current_user)
    messages = Message.query.filter_by(chatid=id).order_by('timestamp')
    form  = AddMessageForm()
    leavechatform = LeaveChatForm()
    if form.validate_on_submit():
        message = Message(text = form.text.data, userid = current_user.id, chatid = id)
        insert_to_db(message)
        flash('The message has been updated.')
        return redirect(url_for('main.show_chat',id = id))
    if  leavechatform.validate_on_submit():
        chat.chat_partisipants.remove(current_user)
        return redirect(url_for('main.show_chats',username = current_user.username))
    return render_template('chat.html', messages = messages, current_user = current_user, form = form, \
                           leavechatform = leavechatform)


@main.route('/leave_chat/<int:id>', methods=['POST'])
@login_required
def leave_chat(id):
    chat = Chat.query.filter_by(id = id).first()
    chat.chat_partisipants.remove(current_user)
    return redirect(url_for('main.show_chats',username = current_user.username))