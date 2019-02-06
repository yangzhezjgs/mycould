from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class TextForm(FlaskForm):
    text = TextAreaField('', 
        validators=[DataRequired(), Length(1, 200)],
        render_kw={
            "class": "form-control",
            "placeholder": "请输入待做事项"
        }
    )
    submit = SubmitField(
        render_kw={
            "class": "btn btn-primary"
        }
    )