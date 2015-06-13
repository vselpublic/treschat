from flask.ext.wtf import Form
from flask.ext.pagedown.fields import PageDownField
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
SubmitField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError


class AddChatForm(Form):
    chatname = PageDownField("Name your chat!", validators=[Required()])
    submit = SubmitField('Go for Chating!')


class AddMessageForm(Form):
    text = PageDownField("TresChi!", validators=[Required()])
    submit = SubmitField('Send!')


class LeaveChatForm(Form):
    submit = SubmitField('Leave Chat!')