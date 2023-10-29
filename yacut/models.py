from datetime import datetime
from random import choices

from flask import url_for

from settings import (ORIGINAL_LINK_LENGTH, REDIRECT_VIEW,
                      SHORT_LENGTH, SHORT_REGEX, SHORT_SIZE, SYMBOLS)

from . import db
from .exceptions import (IncorrectOriginalURLException,
                         IncorrectShortURLException, NonUniqueException)


SHORT_URL_NAME_ALREADY_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'
SHORT_URL_INCORRECT_NAME = 'Указано недопустимое имя для короткой ссылки'
INCORRECT_SYMBOLS_IN_URL = 'Используются некорректные символы'
FAIL_TO_GENERATE = 'Не удалось сгенерировать короткий идентификатор'
LIMIT_OF_SYMBOLS = 'Ссылка превысила лимит символов'


class URLMap(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    original = db.Column(
        db.Text(ORIGINAL_LINK_LENGTH),
        nullable=False,
    )
    short = db.Column(
        db.String(SHORT_LENGTH),
        nullable=False,
        unique=True,
    )
    timestamp = db.Column(
        db.DateTime,
        index=True,
        default=datetime.utcnow,
    )

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                REDIRECT_VIEW,
                short=self.short,
                _external=True,
            )
        )

    @staticmethod
    def create(original, short=None, is_validate=True):
        if is_validate:
            if len(original) > ORIGINAL_LINK_LENGTH:
                raise IncorrectOriginalURLException(
                    LIMIT_OF_SYMBOLS.format('Оригинальная')
                )
            if short:
                if len(short) > SHORT_LENGTH:
                    raise IncorrectShortURLException(
                        LIMIT_OF_SYMBOLS.format('Короткая')
                    )
                if URLMap.get(short):
                    raise NonUniqueException(
                        SHORT_URL_NAME_ALREADY_EXISTS.format(short)
                    )
                if not SHORT_REGEX.match(short):
                    raise IncorrectShortURLException(INCORRECT_SYMBOLS_IN_URL)

        url_map = URLMap(
            original=original,
            short=short or URLMap.create_short()
        )
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def create_short():
        for _ in range(SHORT_SIZE):
            short = ''.join((choices(SYMBOLS, k=SHORT_SIZE)))
            if not URLMap.get(short):
                return short
        raise IncorrectShortURLException(FAIL_TO_GENERATE)

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_or_404(short):
        return URLMap.query.filter_by(short=short).first_or_404().original
