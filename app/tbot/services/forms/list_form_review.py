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
        if review == 'boss':
            reviews = self.cut_per_page(reviews, page)
            unique_args = [{'review': review.id} for review in reviews]
            main_template = BUTTONS_TEMPLATES['boss_review_form']
            update_template = BUTTONS_TEMPLATES['boss_review_update_list']
            pagination_template = BUTTONS_TEMPLATES['boss_review_list']
            asc_template = BUTTONS_TEMPLATES['boss_review_sort_asc']
            desc_template = BUTTONS_TEMPLATES['boss_review_sort_desc']
            self.add_sorting(asc=asc_template, desc=desc_template, is_asc=is_asc)
            self.add_paginator(paginator=pagination_template, page=page, count_obj=len(forms))
            self.add_update(update=update_template)
            return self.build_list(main_template, unique_args)

        elif review == 'coworker':
            reviews = self.cut_per_page(reviews, page)
            unique_args = [{'review': review.id} for review in reviews]
            update_template = BUTTONS_TEMPLATES['coworker_review_update_list']
            pagination_template = BUTTONS_TEMPLATES['coworker_review_list']
            asc_template = BUTTONS_TEMPLATES['coworker_review_sort_asc']
            desc_template = BUTTONS_TEMPLATES['coworker_review_sort_desc']
            main_template = BUTTONS_TEMPLATES['coworker_review_form']
            self.add_sorting(asc=asc_template, desc=desc_template, is_asc=is_asc)
            self.add_paginator(paginator=pagination_template, page=page, count_obj=len(forms))
            self.add_update(update=update_template)
            return self.build_list(main_template, unique_args)

        elif review == 'hr':
            update_template = BUTTONS_TEMPLATES['hr_review_update_list']
            pagination_template = BUTTONS_TEMPLATES['hr_review_list']
            asc_template = BUTTONS_TEMPLATES['hr_review_sort_asc']
            desc_template = BUTTONS_TEMPLATES['hr_review_sort_desc']
            main_template = BUTTONS_TEMPLATES['hr_review_form']
            unique_args = [{'review': review.id} for review in reviews]
            self.add_sorting(asc=asc_template, desc=desc_template, is_asc=is_asc)
            self.add_paginator(paginator=pagination_template, page=page, count_obj=len(forms))
            self.add_update(update=update_template)
            return self.build_list(main_template, unique_args)

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """
        forms = self.args.get('forms')
        advices = self.args.get('advices')
        review = self.args.get('review')
        reviews = self.args.get('reviews')
        page = self.args.get('page')

        title = '[СПИСОК АНКЕТ НА ПРОВЕРКУ]'
        if review == 'boss':
            description = 'Можете выбрать форму подчинённого на проверку.'
            list_data = [f'@{review.form.user.username}' for review in reviews]
            self.build_list_message(title=title,
                                    description=description,
                                    list_text=list_data)
            return self.MESSAGE

        elif review == 'coworker':
            description = 'Можете выбрать форму коллеги на оценку.'
            reviews = self.cut_per_page(reviews, page)
            list_data = [f'{review.advice.form.user.fullname}' for review in reviews]
            self.build_list_message(title=title,
                                    description=description,
                                    list_text=list_data)
            return self.MESSAGE

        elif review == 'hr':
            description = 'Можете выбрать форму на проверку'
            reviews = self.cut_per_page(reviews, page)
            list_data = [f'@{review.advice.form.user.username} - @{review.coworker.username}' for review in reviews]
            self.build_list_message(title=title,
                                    description=description,
                                    list_text=list_data)
            return self.MESSAGE


__all__ = ['ListFormReview']
