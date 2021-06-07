from typing import Optional

from telebot.types import InlineKeyboardMarkup

from app.services.form_review.project_comments import ProjectCommentService
from app.tbot.extensions.template import Template
from app.tbot.storages import BUTTONS_TEMPLATES


class ArchiveForm(Template):
    """ Шаблон формы архива """

    def create_markup(self) -> Optional[InlineKeyboardMarkup]:
        """ Создать клавиатуру """
        page = self.args.get('page')
        old_forms = self.args.get('old_forms')
        old_reviews = self.args.get('old_reviews')

        if old_reviews and self.args.get('review_list'):
            count_obj = len(old_reviews)
            reviews = self.cut_per_page(old_reviews, page)
            unique_args = [{'pk': review.id} for review in reviews]
            main_template = BUTTONS_TEMPLATES['get_old_review']
            pagination_template = BUTTONS_TEMPLATES['old_review_list']
            self.add_paginator(paginator=pagination_template, page=page, count_obj=count_obj)
            return self.build_list(main_template, unique_args)
        elif old_forms and self.args.get('archive_list'):
            count_obj = len(old_forms)
            old_forms = self.cut_per_page(old_forms, page)
            unique_args = [{'pk': form.id} for form in old_forms]
            main_template = BUTTONS_TEMPLATES['get_rapport'].add(period_id=self.args.get('period_id'))
            pagination_template = BUTTONS_TEMPLATES['get_old_review']
            back = BUTTONS_TEMPLATES['back_to_old_review_list']
            self.extend_keyboard(False, back)
            self.add_paginator(paginator=pagination_template, page=page, count_obj=count_obj)
            return self.build_list(main_template, unique_args)
        elif self.args.get('pk') and self.args.get('choose_rapport'):
            rows = list()
            rows.append([BUTTONS_TEMPLATES['get_hr_rapport'].add(form_id=self.args.get('pk')),
                         BUTTONS_TEMPLATES['get_boss_rapport'].add(form_id=self.args.get('pk'))])
            rows.append([BUTTONS_TEMPLATES['send_rapport_to_boss'].add(form_id=self.args.get('pk'))])
            if self.args.get('period_id'):
                rows.append([BUTTONS_TEMPLATES['back_to_rapport']
                            .add(pk=self.args.get('period_id'))])
            else:
                rows.append([BUTTONS_TEMPLATES['back_to_form']
                            .add(pk=self.args.get('pk'))])
            markup = self.markup_builder.build(*rows)
            return markup

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """
        old_forms = self.args.get('old_forms')
        old_reviews = self.args.get('old_reviews')
        page = self.args.get('page')
        if page:
            old_reviews = self.cut_per_page(old_reviews, page) if old_reviews else None
            old_forms = self.cut_per_page(old_forms, page) if old_forms else None

        if old_reviews and self.args.get('review_list'):
            title = 'Архив'
            description = 'Выберите номер Review, чтобы посмотреть анкеты:'
            list_data = list()
            for model in old_reviews:
                start_date = model.start_date.date().strftime("%d.%m.%Y")
                end_date = model.end_date.date().strftime("%d.%m.%Y")
                string = f'Ревью с {start_date} по {end_date}\n'
                list_data.append(string)

            message_text = self.message_builder.build_list_message(title=title,
                                                                   description=description,
                                                                   list_data=list_data,
                                                                   )
        elif old_forms and self.args.get('archive_list'):
            start_date = old_forms[0].review_period.start_date.date().strftime("%d.%m.%Y")
            end_date = old_forms[0].review_period.end_date.date().strftime("%d.%m.%Y")
            title = f'Период Review {start_date} - {end_date}'
            description = 'Выберите номер анкеты, чтобы сформировать отчет:'
            list_data = list()
            for model in old_forms:
                string = f'{model.user.fullname},\n{model.status.name}'
                rating = ProjectCommentService().final_rating(model.id)
                string += f",\nОценка: {rating}\n" if rating else "\n"
                list_data.append(string)

            message_text = self.message_builder.build_list_message(title=title,
                                                                   description=description,
                                                                   list_data=list_data,
                                                                   )
        elif self.args.get('pk') and self.args.get('choose_rapport'):
            text = 'Для кого предназначена выгрузка?'
            message_text = self.message_builder.build_message('', '', text=text)
        elif self.args.get('sent_to_boss'):
            text = 'Отчет отправлен руководителю.'
            message_text = self.message_builder.build_message('', '', text=text)
        elif self.args.get('no_boss'):
            text = 'У пользователя нет руководителя.'
            message_text = self.message_builder.build_message('', '', text=text)
        else:
            text = 'Нет завершенных Review. ' \
                   'Вы можете остановить его в разделе "Запуск/остановка Review"'
            message_text = self.message_builder.build_message('', '', text=text)

        return message_text


__all__ = ['ArchiveForm']
