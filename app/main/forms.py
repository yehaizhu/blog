# -*- coding: utf-8 -*-
from flask_pagedown.fields import PageDownField
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required


class PostForm(Form):
    title = StringField(label=u'标题', validators=[Required()])
    body = PageDownField(u"文章内容", validators=[Required()])
    submit = SubmitField(u'提交')

class CommentForm(Form):
    body = PageDownField(label=u'评论', validators=[Required()])
    submit = SubmitField(u'提交')


