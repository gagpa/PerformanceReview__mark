from typing import Optional

from telebot.types import InlineKeyboardMarkup

from app.tbot.extensions.template import Template
from app.tbot.storages import BUTTONS_TEMPLATES


class AchievementForm(Template):
    """ Шаблон формы достижений """

    def create_markup(self) -> Optional[InlineKeyboardMarkup]:
        """ Создать клавиатуру """
        if self.args.get('can_edit'):
            row = [BUTTONS_TEMPLATES['form']]
            markup = self.markup_builder.build(row, pk=self.args['model'].id)
            return markup

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """
        title = '[Достижение]'

        if not self.args.get('can_edit'):
            description = 'Отправьте в сообщении свои основные достижения и успехи'
            text = f'{self.args["model"].text}'

        else:
            description = ''
            text = ''

        message_text = self.message_builder.build_message(title=title,
                                                          description=description,
                                                          text=text,
                                                          )
        return message_text


__all__ = ['AchievementForm']
