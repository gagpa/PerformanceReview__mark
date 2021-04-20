from typing import Optional, Tuple

from telebot.types import InlineKeyboardMarkup

from app.tbot.extensions import InlineKeyboardBuilder
from app.tbot.extensions.template import Template
from app.tbot.storages import BUTTONS_TEMPLATES


class ListFormReview(Template):
    """ Шаблон списка анкет на проверку """

    def create_markup(self) -> InlineKeyboardMarkup:
        """ Создать клавиатуру """
        if self.args.get('models'):
            if self.args.get('on_boss_review'):
                return InlineKeyboardBuilder.build_list(self.args['models'], BUTTONS_TEMPLATES['boss_review_form'])

            elif self.args.get('on_coworker_review'):
                return InlineKeyboardBuilder.build_list(self.args['models'], BUTTONS_TEMPLATES['coworker_review_form'])

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """
        title = '[СПИСОК АНКЕТ НА ПРОВЕРКУ]'

        if self.args.get('models'):
            if self.args.get('on_boss_review'):
                description = 'Можете выбрать форму подчинённого на проверку.'
                list_data = [f'{self.model.user.fullname}' for self.model in self.args['models']]
                return self.message_builder.build_list_message(title=title,
                                                               description=description,
                                                               list_data=list_data,
                                                               )
            elif self.args.get('on_coworker_review'):
                description = 'Можете выбрать форму коллеги на оценку.'
                list_data = [f'{self.model.user.fullname}' for self.model in self.args['models']]
                return self.message_builder.build_list_message(title=title,
                                                               description=description,
                                                               list_data=list_data,
                                                               )
        else:
            description = ''
            text = 'Нет форм на проверку'
            return self.message_builder.build_message(title=title, description=description, text=text)


__all__ = ['ListFormReview']
