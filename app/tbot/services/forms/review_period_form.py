from typing import Optional

from telebot.types import InlineKeyboardMarkup

from app.tbot.extensions.template import Template
from app.tbot.storages import BUTTONS_TEMPLATES


class ReviewPeriodForm(Template):
    """ Шаблон формы периода ревью """

    def create_markup(self) -> Optional[InlineKeyboardMarkup]:
        """ Создать клавиатуру """
        rows = []

        if self.args.get('start'):
            rows.append([BUTTONS_TEMPLATES['review_period_start']])
            markup = self.markup_builder.build(*rows)
            return markup
        elif self.args.get('stop'):
            rows.append([BUTTONS_TEMPLATES['review_period_stop']])
            markup = self.markup_builder.build(*rows)
            return markup
        elif self.args.get('choose_first_date_period'):
            markup = self.markup_builder.build_calendar('first_date_period')
            return markup
        elif self.args.get('date') and self.args.get('choose_second_date_period'):
            date = self.args.get('date').strftime("%d-%m-%Y")
            # TODO:  поменять callback
            markup = self.markup_builder.build_calendar(f'date_period_2|{date}')
            return markup

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """
        text = ''
        description = ''

        if self.args.get('start'):
            title = 'Review еще не запущено'
            message_text = self.message_builder.build_message(title=title,
                                                              description=description,
                                                              text=text,
                                                              )
        elif self.args.get('model') and self.args.get('stop'):
            title = 'Review запущено'
            message_text = self.message_builder.build_message(title=title,
                                                              description=description,
                                                              text=text,
                                                              )
        elif self.args.get('choose_first_date_period'):
            title = 'Выберите дату начала Review'
            message_text = self.message_builder.build_message(title=title,
                                                              description=description,
                                                              text=text,
                                                              )
        elif self.args.get('choose_second_date_period'):
            title = 'Выберите дату окончания Review'
            message_text = self.message_builder.build_message(title=title,
                                                              description=description,
                                                              text=text,
                                                              )
        elif self.args.get('stopped'):
            title = 'Текущие Review остановлено'
            message_text = self.message_builder.build_message(title=title,
                                                              description=description,
                                                              text=text,
                                                              )
        elif self.args.get('started'):
            title = 'Новое Review запущено'
            message_text = self.message_builder.build_message(title=title,
                                                              description=description,
                                                              text=text,
                                                              )
        elif self.args.get('cancel'):
            title = 'Календарь закрыт.'
            message_text = self.message_builder.build_message(title=title,
                                                              description=description,
                                                              text=text,
                                                              )
        else:
            message_text = self.message_builder.build_message('', '', 'Нет Review')

        return message_text


__all__ = ['ReviewPeriodForm']
