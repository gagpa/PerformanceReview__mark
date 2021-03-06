from typing import Optional

from telebot.types import InlineKeyboardMarkup

from app.services.dictinary import StatusService
from app.services.form_review.project_comments import ProjectCommentService
from app.services.review import HrReviewService
from app.tbot.extensions.template import Template
from app.tbot.storages import BUTTONS_TEMPLATES
from app import queries
from app.pkgs import mark_calculator as calculators
from app.pkgs.report import create_form_frame


def cut_middle(fullname):
    return ' '.join(fullname.split(' ')[:2])


def get_marks_info(form):
    avr_lead = calculators.LeadCalculator.calculate(form)
    avr_coworkers = calculators.CoworkerCalculator.calculate(form)
    avr_subordinates = calculators.SubordinateCalculator.calculate(form)
    lead_marks = queries.find__lead_marks(form).all()
    form_frame = create_form_frame(form)
    text = ''
    if lead_marks:
        if avr_lead:
            text += f'<b>Руководитель: {avr_lead}</b>\n' \
                    f'{cut_middle(form_frame.author.lead.fullname)} @{form_frame.author.lead.username}: {avr_lead}'
        elif [mark for mark in lead_marks if mark.rating and mark.rating.value == -1]:
            text += f'<b>Руководитель: не могу оценить</b>\n' \
                    f'{cut_middle(form_frame.author.lead.fullname)} @{form_frame.author.lead.username}'
        else:
            text += f'<b>Руководитель: не оценил</b>\n' \
                    f'{cut_middle(form_frame.author.lead.fullname)} @{form_frame.author.lead.username}'
    else:
        text += f'<b>Нет руководителя</b>'
    if avr_coworkers:
        text += f'\n<b>Коллеги: {avr_lead}</b>\n'
        for coworker in form_frame.respondents:
            if coworker.employee.relation == 'коллега' and coworker.average_mark:
                text += f'{cut_middle(coworker.employee.fullname)} @{coworker.employee.username}: {coworker.average_mark}\n'
    else:
        is_first = True
        for coworker in form_frame.respondents:
            if coworker.employee.relation == 'коллега':
                if [mark.mark for mark in coworker.marks if mark.mark == -1]:
                    if is_first:
                        text += f'\n<b>Коллеги: нет</b>'
                        is_first = False
                    text += f'\n{cut_middle(coworker.employee.fullname)} @{coworker.employee.username}: не могу оценить'
    if avr_subordinates:
        text += f'\n<b>Подчинённые: {avr_subordinates}</b>\n'
        for coworker in form_frame.respondents:
            if coworker.employee.relation == 'подчинённый' and coworker.average_mark:
                text += f'{cut_middle(coworker.employee.fullname)} @{coworker.employee.username}: {coworker.average_mark}\n'
    else:
        is_first = True
        for coworker in form_frame.respondents:
            if coworker.employee.relation == 'подчинённый':
                if is_first:
                    text += f'\n<b>Подчинённые: нет</b>\n'
                    is_first = False
                if [mark.mark for mark in coworker.marks if mark.mark == -1]:
                    text += f'\n{cut_middle(coworker.employee.fullname)} @{coworker.employee.username}: не могу оценить'
                else:
                    text += f'\n{cut_middle(coworker.employee.fullname)} @{coworker.employee.username}: не оценил'
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
            self.build_message(title='Review сотрудника')
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
            rating = self.args.get('rating') if self.args.get('rating') else 'остутствует'
            marks = get_marks_info(self.args.get('model'))
            self.build_message(text=f'<i>ФИО:</i> {self.args.get("model").user.fullname}\n'
                                    f'<i>Статус:</i> {self.args.get("model").status.name}')
            self.build_message(text=f'▪️<b>Оценка:</b> {rating}')
            self.build_message(text=f'{marks}')
            self.build_message(title=f'▪️Что делать:\n'
                                     f'{todo if todo else "отсутствует"}')
            self.build_message(title=f'▪️Что не делать:\n'
                                     f'{not_todo if not_todo else "отсутствует"}')
            self.build_message(title=f'▪️Подведение итогов:\n'
                                     f'{summary}')
            if self.args.get('summary'):
                self.build_message(f'❕ Доступна опция выгрузки анкеты')
            if not_rated:
                self.build_message(f'❕ Не оценили:\n'
                                   f'{usernames}')
            return self.MESSAGE
        elif self.args.get('change_summary'):
            self.build_message(title='Review сотрудника')
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
            rating = self.args.get('rating') if self.args.get('rating') else 'отсутствует'
            marks = get_marks_info(self.args.get('model'))
            self.build_message(text=f'<i>ФИО:</i> {self.args.get("model").user.fullname}\n'
                                    f'<i>Статус:</i> {self.args.get("model").status.name}')
            self.build_message(text=f'▪️<b>Оценка:</b> {rating}')
            self.build_message(text=f'{marks}')
            self.build_message(title=f'▪️Что делать:\n'
                                     f'{todo if todo else "отсутствует"}')
            self.build_message(title=f'▪️Что не делать:\n'
                                     f'{not_todo if not_todo else "отсутствует"}')
            self.build_message(title=f'▪️Подведение итогов:\n'
                                     f'{summary}')
            self.build_message(description='❕ Введите краткие итоги на основе полученных советов:')
            return self.MESSAGE
        elif self.args.get('changed'):
            text = 'Итоги сформированы. Доступна опция выгрузки анкеты.'
            message_text = self.message_builder.build_message('', '', text=text)
        else:
            text = 'Review не запущен, Вы можете запустить его в разделе "Запуск/остановка Review"'
            message_text = self.message_builder.build_message('', '', text=text)

        return message_text


__all__ = ['CurrentReviewForm']
