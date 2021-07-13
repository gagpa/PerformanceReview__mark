from typing import Optional

from telebot.types import InlineKeyboardMarkup

from app.services.dictinary import StatusService
from app.services.form_review.project_comments import ProjectCommentService
from app.services.review import HrReviewService
from app.tbot.extensions.template import Template
from app.tbot.storages import BUTTONS_TEMPLATES


def get_marks_info(marks, boss, coworkers, subordinate):
    text = '\n'
    if boss != 'Нет':
        text += f'\n<b>Руководитель: {boss}</b>'
        text += ''.join(marks['Руководитель'][0])
    if coworkers != 'Нет':
        text += f'\n\n<b>Коллеги: {coworkers}</b>'
        text += '\n'.join(marks['Коллеги'])
    if subordinate != 'Нет':
        text += f'\n\n<b>Подчиненные: {subordinate}</b>'
        text += '\n'.join(marks['Подчиненные'])
    return text


class CurrentReviewForm(Template):
    """ Шаблон формы текущего Review """

    def create_markup(self) -> Optional[InlineKeyboardMarkup]:
        """ Создать клавиатуру """
        forms = self.args.get('models')
        page = self.args.get('page')
        if forms and self.args.get('forms_list'):
            count_obj = len(forms)
            forms = self.cut_per_page(forms, page)
            unique_args = [{'pk': form.id} for form in forms]
            main_template = BUTTONS_TEMPLATES['employee_review']
            pagination_template = BUTTONS_TEMPLATES['current_forms_list']
            self.add_paginator(paginator=pagination_template, page=page, count_obj=count_obj)
            return self.build_list(main_template, unique_args)
        elif self.args.get('model') and not self.args.get('summary'):
            rows = list()
            if self.args.get('model').status.name == 'Анкета заполена':
                rows.append(
                    [BUTTONS_TEMPLATES['input_summary'].add(form_id=self.args.get('model').id),
                     BUTTONS_TEMPLATES['current_forms_list_back']])
            else:
                rows.append([BUTTONS_TEMPLATES['current_forms_list']])
            markup = self.markup_builder.build(*rows)
            return markup
        elif self.args.get('model') and self.args.get('summary'):
            rows = list()
            rows.append(
                [BUTTONS_TEMPLATES['change_summary'].add(form_id=self.args.get('model').id),
                 BUTTONS_TEMPLATES['get_current_rapport'].add(pk=self.args.get('model').id)])
            rows.append([BUTTONS_TEMPLATES['current_forms_list']])
            markup = self.markup_builder.build(*rows)
            return markup

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """
        description = ''
        forms = self.args.get('models')
        page = self.args.get('page')
        if page:
            forms = self.cut_per_page(forms, page) if forms else None

        if forms and self.args.get('forms_list'):
            title = 'Текущий Review'
            list_data = list()
            for model in forms:
                string = f'{model.user.fullname}\n{model.status.name}'
                rating = ProjectCommentService().final_rating(model.id)
                if model.status in [StatusService().accepted, StatusService().review_done]:
                    string += f"\nОценка: {rating}\n" if rating else "\n"
                else:
                    string += '\n'
                list_data.append(string)

            message_text = self.message_builder.build_list_message(title=title,
                                                                   description=description,
                                                                   list_data=list_data,
                                                                   )
        elif self.args.get('model') and not self.args.get('change_summary'):
            title = 'Review сотрудника'
            todo = []
            not_todo = []
            not_rated = HrReviewService().not_rated(self.args.get('form_id'))
            usernames = '\n'.join(not_rated)
            for advice in self.args.get('advices'):
                if advice.advice_type.name == 'todo':
                    todo.append(f'• {advice.text}')
                else:
                    not_todo.append(f'• {advice.text}')
            todo = '\n'.join(todo)
            not_todo = '\n'.join(not_todo)
            summary = self.args.get('summary').text if self.args.get('summary') else 'отсутствует'
            rating = self.args.get('rating') if self.args.get('rating') else '\nостутствует'
            marks = get_marks_info(self.args.get('marks'), self.args.get('boss_rating'),
                                   self.args.get('coworkers_rating'),
                                   self.args.get('subordinate_rating'))
            text = f"<i>ФИО:</i> {self.args.get('model').user.fullname}\n" \
                   f"<i>Статус:</i> {self.args.get('model').status.name}\n\n" \
                   f"▪️<b>Оценка:</b> {rating}" \
                   f"{marks}\n" \
                   f"\n▪️<b>Что делать:</b>\n" \
                   f"{todo if todo else 'отсутствует'}" \
                   f"\n\n▪️<b>Что не делать:</b>\n" \
                   f"{not_todo if not_todo else 'отсутствует'}" \
                   f"\n\n▪️<b>Подведение итогов:</b>" \
                   f"\n{summary}"
            if self.args.get('summary'):
                text = f'{text}\n\n❕ Доступна опция выгрузки анкеты'
            if not_rated:
                text = f'{text}\n\n❕ Не оценили:\n{usernames}'
            message_text = self.message_builder.build_message(title, '', text)
        elif self.args.get('change_summary'):
            title = 'Review сотрудника'
            todo = []
            not_todo = []
            for advice in self.args.get('advices'):
                if advice.advice_type.name == 'todo':
                    todo.append(f'• {advice.text}')
                else:
                    not_todo.append(f'• {advice.text}')
            todo = '\n'.join(todo)
            not_todo = '\n'.join(not_todo)
            summary = self.args.get('summary').text if self.args.get('summary') else 'отсутствует'
            rating = self.args.get('rating') if self.args.get('rating') else '\nостутствует'
            text = f"<i>ФИО:</i> {self.args.get('model').user.fullname}\n" \
                   f"<i>Статус:</i> {self.args.get('model').status.name}\n\n" \
                   f"<b>Оценка:</b> {rating}\n" \
                   f"\n<b>Что делать:</b>\n" \
                   f"{todo if todo else 'отсутствует'}" \
                   f"\n\n<b>Что не делать:</b>\n" \
                   f"{not_todo if not_todo else 'отсутствует'}" \
                   f"\n\n<b>Подведение итогов:</b>" \
                   f"\n{summary}"

            text += '\n\n❕ Введите краткие итоги на основе полученных советов:'
            message_text = self.message_builder.build_message(title, '', text=text)
        elif self.args.get('changed'):
            text = 'Итоги сформированы. Доступна опция выгрузки анкеты.'
            message_text = self.message_builder.build_message('', '', text=text)
        else:
            text = 'Review не запущен, Вы можете запустить его в разделе "Запуск/остановка Review"'
            message_text = self.message_builder.build_message('', '', text=text)

        return message_text


__all__ = ['CurrentReviewForm']
