from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    picture = FileField('picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    comment = StringField('Comment', validators=[DataRequired()])
    submit1 = SubmitField('Submit')

class ReactForm(FlaskForm):
	submit2 = SubmitField('Upvote')

class DisReactForm(FlaskForm):
	submit3 = SubmitField('Down vote')

