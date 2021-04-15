from typing import Optional

from telebot.types import InlineKeyboardMarkup

from app.tbot.extensions.template import Template
from app.tbot.storages import BUTTONS_TEMPLATES


class ArchiveForm(Template):
    """ Шаблон формы архива """

    def create_markup(self) -> Optional[InlineKeyboardMarkup]:
        """ Создать клавиатуру """
        if self.args.get('models') and self.args.get('archive_list'):
            row = BUTTONS_TEMPLATES['get_rapport']
            markup = self.markup_builder.build_list(self.args['models'], row)
            return markup
        elif self.args.get('pk') and self.args.get('choose_rapport'):
            rows = list()
            rows.append([BUTTONS_TEMPLATES['get_hr_rapport'].add(pk=self.args.get('pk')),
                         BUTTONS_TEMPLATES['get_boss_rapport'].add(pk=self.args.get('pk'))])
            markup = self.markup_builder.build(*rows)
            return markup

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """
        description = ''

        if self.args.get('models') and self.args.get('archive_list'):
            title = 'Архив'
            list_data = [f'{model.user.fullname},\n' \
                         f'{model.status.name},\n' \
                         f'{model.review_period.start_date.date()} - {model.review_period.end_date.date()},\n' \
                         f'Оценка: {model.rating.name}\n' for model in self.args["models"]]
            message_text = self.message_builder.build_list_message(title=title,
                                                                   description=description,
                                                                   list_data=list_data,
                                                                   )
        elif self.args.get('pk') and self.args.get('choose_rapport'):
            text = 'Для кого предназначена выгрузка?'
            message_text = self.message_builder.build_message('', '', text=text)
        else:
            text = 'Нет завершенных Review. ' \
                   'Вы можете остановить его в разделе "Запуск/остановка Review"'
            message_text = self.message_builder.build_message('', '', text=text)

        return message_text


__all__ = ['ArchiveForm']
