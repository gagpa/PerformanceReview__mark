from telebot.types import InlineKeyboardMarkup

from app.tbot.extensions import InlineKeyboardBuilder
from app.tbot.extensions.template import Template
from app.tbot.storages import BUTTONS_TEMPLATES


class DutyForm(Template):
    """ Шаблон формы обязанностей """

    def create_markup(self) -> InlineKeyboardMarkup:
        """ Создать клавиатуру """
        rows = []
        if self.args.get('can_add'):
            rows.append([BUTTONS_TEMPLATES['review_form_duty_add']])
            rows.append([BUTTONS_TEMPLATES['review_form']])
            markup = InlineKeyboardBuilder.build(*rows)
            return markup

        elif self.args.get('can_edit'):
            rows.append([BUTTONS_TEMPLATES['review_form_duty_edit']])
            rows.append([BUTTONS_TEMPLATES['review_form']])
            markup = InlineKeyboardBuilder.build(*rows)
            return markup

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """
        title = '▪️Обязанности'
        model = self.args.get('model')
        if self.args.get('can_add'):
            description = 'Функционал, который ты выполняешь в ходе своей работы'
            text = self.args['model'].text if self.args['model'] else ''

        elif self.args.get('can_edit'):
            description = '\nВнесите изменения или вернитесь к анкете'
            text = f' -  {self.args["model"].text}'

        elif self.args.get('form'):
            if model:
                text = self.args['model'].text
            else:
                text = 'Не заполнено'
            message_text = self.message_builder.build_message(title=title,
                                                              text=text,
                                                              )
            return message_text

        else:
            description = 'Отправьте в сообщении свои обязанности'
            text = ''

        message_text = self.message_builder.build_message(title=title,
                                                          description=description,
                                                          text=text,
                                                          )
        return message_text


__all__ = ['DutyForm']
