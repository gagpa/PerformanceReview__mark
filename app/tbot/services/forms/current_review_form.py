from typing import Optional

from telebot.types import InlineKeyboardMarkup

from app.tbot.extensions.template import Template
from app.tbot.storages import BUTTONS_TEMPLATES


class CurrentReviewForm(Template):
    """ Шаблон формы текущего Review """

    def create_markup(self) -> Optional[InlineKeyboardMarkup]:
        """ Создать клавиатуру """
        if self.args.get('models') and self.args.get('forms_list'):
            row = BUTTONS_TEMPLATES['employee_review']
            markup = self.markup_builder.build_list(self.args['models'], row)
            return markup
        elif self.args.get('model') and not self.args.get('summary'):
            rows = list()
            rows.append([BUTTONS_TEMPLATES['input_summary'].add(pk=self.args.get('model').id),
                         BUTTONS_TEMPLATES['current_forms_list']])
            markup = self.markup_builder.build(*rows)
            return markup
        elif self.args.get('model') and self.args.get('summary'):
            rows = list()
            rows.append([BUTTONS_TEMPLATES['change_summary'].add(pk=self.args.get('model').id),
                         BUTTONS_TEMPLATES['get_current_rapport'].add(
                             pk=self.args.get('model').id),
                         BUTTONS_TEMPLATES['current_forms_list']])
            markup = self.markup_builder.build(*rows)
            return markup

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """
        description = ''

        if self.args.get('models') and self.args.get('forms_list'):
            title = 'Текущий Review'
            rating = self.args.get("rating")
            list_data = [f'{model.user.fullname},\n' \
                         f'{model.status.name},\n' \
                         f'{f"Оценка: {rating}" if rating and model.status.id == 4 else ""}\n'
                         for model in self.args["models"]]
            message_text = self.message_builder.build_list_message(title=title,
                                                                   description=description,
                                                                   list_data=list_data,
                                                                   )
        elif self.args.get('model'):
            title = 'Review сотрудника'
            to_do = ''
            not_todo = ''
            for advice in self.args.get('advices'):
                to_do += f'{advice.todo}\n'
                not_todo += f'{advice.not_todo}\n'
            summary = self.args.get('summary').text if self.args.get('summary') else 'отсутствует'
            rating = self.args.get("rating")
            text = f"ФИО: {self.args.get('model').user.fullname}\n" \
                   f"Статус: {self.args.get('model').status.name}\n" \
                   f"Оценка: {rating}\n" \
                   f"\nЧто делать:\n" \
                   f"{to_do}" if to_do else 'отсутсвует'\
                   f"\nЧто не делать:\n" \
                   f"{not_todo}" if not_todo else 'отсутсвует'\
                   f"\nSummary:" \
                   f"\n{summary}"
            message_text = self.message_builder.build_message(title, '', text)
        elif self.args.get('change_summary'):
            text = 'Введите summaries на основе полученных советов:'
            message_text = self.message_builder.build_message('', '', text=text)
        elif self.args.get('changed'):
            text = 'Summaries сформировано. Доступна опция выгрузки анкеты.'
            message_text = self.message_builder.build_message('', '', text=text)
        else:
            text = 'Review не запущен, Вы можете запустить его в разделе "Запуск/остановка Review"'
            message_text = self.message_builder.build_message('', '', text=text)

        return message_text


__all__ = ['CurrentReviewForm']
