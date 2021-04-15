from typing import Optional

from telebot.types import InlineKeyboardMarkup

from app.tbot.extensions.template import Template
from app.tbot.storages import BUTTONS_TEMPLATES


class CurrentReviewForm(Template):
    """ Шаблон формы текущего Review """

    def create_markup(self) -> Optional[InlineKeyboardMarkup]:
        """ Создать клавиатуру """
        if self.args.get('models') and self.args.get('forms_list'):
            row = BUTTONS_TEMPLATES['get_rapport']
            markup = self.markup_builder.build_list(self.args['models'], row)
            return markup

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """
        description = ''

        if self.args.get('models') and self.args.get('forms_list'):
            title = 'Текущий Review'
            list_data = [f'{model.user.fullname},\n' \
                         f'{model.status.name},\n' \
                         f'{f"Оценка: {model.rating.name}" if model.rating else ""}\n' for
                         model in self.args["models"]]
            message_text = self.message_builder.build_list_message(title=title,
                                                                   description=description,
                                                                   list_data=list_data,
                                                                   )
        else:
            text = 'Review не запущен, Вы можете запустить его в разделе "Запуск/остановка Review"'
            message_text = self.message_builder.build_message('', '', text=text)

        return message_text


__all__ = ['CurrentReviewForm']
