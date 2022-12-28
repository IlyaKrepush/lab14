from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, FileField, IntegerField, SubmitField, EmailField
from wtforms.validators import Length, Email, EqualTo, DataRequired, ValidationError 
import string
from table import Users


class ProductForm(FlaskForm):
    type=StringField("type")
    name=StringField("name")
    description=TextAreaField("description")
    manufacturer=StringField("manufacturer")
    price=IntegerField("price")
    photo=FileField("photo")
    submit=SubmitField("create new product")


key_symbol_symbol = "%$#@&*^|\/~[]{},.:;?!-()<>"
key_symbol_chisl = "0123456789"
key_symbol_login = str(string.ascii_letters) + "_" + key_symbol_chisl
upper = list(string.ascii_uppercase)

class CreateUserForm(FlaskForm):
    username = StringField(label=('Username'),
                           validators=[DataRequired(),
                                       Length(max=64)])
    email = StringField(label=('Email'),
                        validators=[DataRequired(),
                                    Email(),
                                    Length(max=120)])
    password = StringField(label=("Password"),
                           validators=[DataRequired()])
    password_confired = StringField(label=("Password_confired"),
                                    validators=[DataRequired()])
    submit = SubmitField(label=('Submit'))

    def validate_password(self, password):
        global key_symbol_symbol
        ysl = 0
        char = self.password.data
        for char in self.password.data:
            if char in list(string.ascii_uppercase):
                ysl += 1
                break

        for char in self.password.data:
            if char in list(string.ascii_lowercase):
                ysl += 1
                break
        for char in self.password.data:
            if char in key_symbol_chisl:
                ysl += 1
                break
        for char in self.password.data:
            if char in list(string.ascii_lowercase):
                ysl += 1
                break
        for char in self.password.data:
            if char in key_symbol_symbol:
                ysl += 1
                break

        if ysl != 5 or len(self.password.data) <= 8:
            raise ValidationError(
                f"no capital letter or lowercase letters or symbol" + key_symbol_symbol + "or numbers in password."
            )

    def validate_password_confired(self, password_confired):
        if str(self.password.data) != str(self.password_confired.data):
            raise ValidationError(
                f"Passwords don't match"
            )

    def validate_username(self, username):
        global upper
        global key_symbol_login

        char = str(self.username.data)
        if char[0] not in upper or len(char) <= 6:
            raise ValidationError(
                f"Character {char} is not allowed in username.")
        for char in self.username.data:
            if char not in key_symbol_login:
                raise ValidationError(
                    f"invalid login symbol-{char}.")

class CommentForm(FlaskForm):
    like=IntegerField(label=("like"),
                      validators=[DataRequired()])
    comment=TextAreaField("comment")
    submit=SubmitField("add comment")

    def validate_like(self, like):
        if self.like.data>5 or self.like.data<1:
            raise ValidationError('mark should be about 1-5')