from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, InputRequired, NumberRange, Length

class ContatoForm(FlaskForm):
    # nome = StringField('Nome', validators=[DataRequired()])
    # email = StringField('Email', validators=[DataRequired(), Email()])
    # idade = IntegerField('Idade', validators=[DataRequired()])
    # mensagem = TextAreaField('Mensagem', validators=[DataRequired()])
    
    nome = StringField(
        'Nome', 
        validators=[
            DataRequired(message="O campo de nome é obrigatório."),
            Length(min=2, max=50, message="O nome deve ter entre 2 e 50 caracteres.")
        ]
    )
    email = StringField(
        'Email', 
        validators=[
            DataRequired(message="O campo de email é obrigatório."),
            Email(message="Digite um endereço de email válido.")
        ]
    )
    idade = IntegerField(
        'Idade', 
        validators=[
            InputRequired(message="O campo de idade é obrigatório."),
            NumberRange(min=0, max=120, message="A idade deve estar entre 0 e 120 anos.")
        ]
    )
    mensagem = TextAreaField(
        'Mensagem', 
        validators=[
            DataRequired(message="O campo de mensagem é obrigatório."),
            Length(min=10, max=500, message="A mensagem deve ter entre 10 e 500 caracteres.")
        ]
    )   
    
    enviar = SubmitField('Enviar')
