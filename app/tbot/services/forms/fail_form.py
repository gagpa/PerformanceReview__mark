from telebot.types import InlineKeyboardMarkup

from app.tbot.extensions import InlineKeyboardBuilder
from app.tbot.extensions.template import Template
from app.tbot.storages import BUTTONS_TEMPLATES


class FailForm(Template):
    """ Шаблон формы провала """

    def create_markup(self) -> InlineKeyboardMarkup:
        """ Создать клавиатуру """
        if self.args.get('can_edit'):
            row = [BUTTONS_TEMPLATES['form']]
            markup = InlineKeyboardBuilder.build(row)
            return markup

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """
        title = '[ПРОВАЛ]'

        if not self.args.get('can_edit'):
            description = 'Отправьте в сообщении свой провал или перечислите их через ;'
            text = f'{self.args["model"].text}'

        else:
            description = ''
            text = ''

        message_text = self.message_builder.build_message(title=title,
                                                          description=description,
                                                          text=text,
                                                          )

        return message_text


__all__ = ['FailForm']
