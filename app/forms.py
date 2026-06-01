from flask_wtf import FlaskForm
from wtforms import PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional

from app.constants import (
    INTERACTION_TYPES,
    INTERESSE_LEVELS,
    LEAD_ORIGINS,
    LEAD_STATUSES,
)


class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(), Length(max=120)],
    )
    senha = PasswordField(
        "Senha",
        validators=[DataRequired(), Length(min=6, max=128)],
    )
    submit = SubmitField("Entrar")


class LeadForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired(), Length(max=120)])
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(), Length(max=120)],
    )
    telefone = StringField("Telefone", validators=[Optional(), Length(max=30)])
    empresa = StringField("Empresa", validators=[Optional(), Length(max=120)])
    origem = SelectField(
        "Origem",
        choices=[(o, o) for o in LEAD_ORIGINS],
        validators=[DataRequired()],
    )
    mensagem = TextAreaField("Mensagem", validators=[Optional(), Length(max=2000)])
    segmento = StringField("Segmento", validators=[Optional(), Length(max=120)])
    interesse = SelectField(
        "Interesse (urgencia)",
        choices=[(i, i) for i in INTERESSE_LEVELS],
        validators=[DataRequired()],
    )
    status = SelectField(
        "Status",
        choices=[(s, s) for s in LEAD_STATUSES],
        validators=[DataRequired()],
    )
    submit = SubmitField("Salvar")


class InteractionForm(FlaskForm):
    tipo = SelectField(
        "Tipo",
        choices=[(t, t) for t in INTERACTION_TYPES],
        validators=[DataRequired()],
    )
    mensagem = TextAreaField(
        "Mensagem",
        validators=[DataRequired(), Length(max=2000)],
    )
    submit = SubmitField("Adicionar")
