from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import (URL, DataRequired, Length, Optional, Regexp,
                                ValidationError)

from settings import ORIGINAL_LINK_LENGTH, SHORT_LENGTH, SHORT_REGEX

from .models import URLMap


CREATE = 'Создать'
INCORRECT_ORIGINAL_LINK = 'Ссылка является некорректной'
INCORRECT_SHORT_LINK = 'Используйте только латинские буквы и цифры'
FIELD_SHORT_ID = 'Ваш вариант короткой ссылки'
FIELD_ORIGINAL_LINK = 'Длинная ссылка'
REQUIRED_FIELD = 'Обязательное поле для заполнения'
SHORT_URL_ALREADY_TAKEN = 'Предложенный вариант короткой ссылки уже существует.'


class URLForm(FlaskForm):
    original_link = URLField(
        FIELD_ORIGINAL_LINK,
        validators=[
            DataRequired(REQUIRED_FIELD),
            URL(message=INCORRECT_ORIGINAL_LINK),
            Length(max=ORIGINAL_LINK_LENGTH)
        ]
    )
    custom_id = URLField(
        FIELD_SHORT_ID,
        validators=[
            Optional(),
            Length(max=SHORT_LENGTH),
            Regexp(
                regex=SHORT_REGEX,
                message=INCORRECT_SHORT_LINK
            )
        ]
    )
    submit = SubmitField(CREATE)

    def validate_custom_id(self, field):
        if URLMap.get(field.data):
            raise ValidationError(SHORT_URL_ALREADY_TAKEN.format(field.data))