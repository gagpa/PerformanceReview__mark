from telebot.types import InlineKeyboardMarkup

from app.tbot.extensions.template import Template
from app.tbot.storages import BUTTONS_TEMPLATES


class ListFormReview(Template):
    """ Шаблон списка анкет на проверку """

    def create_markup(self) -> InlineKeyboardMarkup:
        """ Создать клавиатуру """
        forms = self.args.get('forms')
        advices = self.args.get('advices')
        review = self.args.get('review')
        page = self.args.get('page')
        is_asc = self.args.get('is_asc')
        reviews = self.args.get('reviews')
        reviews = self.cut_per_page(reviews, page)
        if review == 'boss':
            count_obj = len(forms)
            unique_args = [{'review': review.id} for review in reviews]
            main_template = BUTTONS_TEMPLATES['boss_review_form']
            update_template = BUTTONS_TEMPLATES['boss_review_update_list']
            pagination_template = BUTTONS_TEMPLATES['boss_review_list']
            self.add_paginator(paginator=pagination_template, page=page, count_obj=count_obj)
            self.add_update(update=update_template)
            return self.build_list(main_template, unique_args)

        elif review == 'coworker':
            count_obj = len(forms)
            unique_args = [{'review': review.id} for review in reviews]
            update_template = BUTTONS_TEMPLATES['coworker_review_update_list']
            pagination_template = BUTTONS_TEMPLATES['coworker_review_list']
            main_template = BUTTONS_TEMPLATES['coworker_review_form']
            self.add_paginator(paginator=pagination_template, page=page, count_obj=count_obj)
            self.add_update(update=update_template)
            return self.build_list(main_template, unique_args)

        elif review == 'hr':
            count_obj = len(forms)
            update_template = BUTTONS_TEMPLATES['hr_review_update_list']
            pagination_template = BUTTONS_TEMPLATES['hr_review_list']
            main_template = BUTTONS_TEMPLATES['hr_review_form']
            unique_args = [{'review': review.id} for review in reviews]
            self.add_paginator(paginator=pagination_template, page=page, count_obj=count_obj)
            self.add_update(update=update_template)
            return self.build_list(main_template, unique_args)

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """
        forms = self.args.get('forms')
        advices = self.args.get('advices')
        review = self.args.get('review')
        reviews = self.args.get('reviews')
        page = self.args.get('page')
        reviews = self.cut_per_page(reviews, page)

        if review == 'boss':
            list_data = [f'@{review.form.user.username} - {review.form.user.fullname}' for review in reviews]
            description = '\n❕ Можете выбрать форму подчинённого на проверку' if list_data else ''
            self.build_list_message(title='📑 Список подчинённых на проверку',
                                    description=description,
                                    list_text=list_data)
            return self.MESSAGE

        elif review == 'coworker':
            list_data = [f'@{review.form.user.username} - {review.form.user.fullname}' for review in reviews]
            description = '\n❕ Можете выбрать форму коллеги на оценку' if list_data else ''
            self.build_list_message(title='📑 Список коллег на оценку',
                                    description=description,
                                    list_text=list_data)
            return self.MESSAGE

        elif review == 'hr':
            list_data = [f'@{review.form.user.username} - @{review.coworker.username}' for review in reviews]
            description = '\n❕ Можете выбрать форму на проверку' if list_data else ''
            self.build_list_message(title='📑 Список оценок и советов на проверку\n\n  Оцениваемый - Оценивающий',
                                    description=description,
                                    list_text=list_data)
            return self.MESSAGE


__all__ = ['ListFormReview']
