from telebot.types import InlineKeyboardMarkup

from app.services.dictinary.rating import RatingService
from app.tbot.extensions import InlineKeyboardBuilder
from app.tbot.extensions.template import Template
from app.tbot.storages import BUTTONS_TEMPLATES


class ProjectForm(Template):
    """ Шаблон формы проектов """

    def create_markup(self) -> InlineKeyboardMarkup:
        """ Создать клавиатуру """
        if self.args.get('can_edit'):
            rows = []

            if self.args.get('is_name'):
                rows.append([BUTTONS_TEMPLATES['review_form_project_edit_description'],
                             BUTTONS_TEMPLATES['review_form_project_edit_contacts']])

            elif self.args.get('is_description'):
                rows.append([BUTTONS_TEMPLATES['review_form_project_edit_name'],
                             BUTTONS_TEMPLATES['review_form_project_edit_contacts']])

            elif self.args.get('is_contacts'):
                rows.append([BUTTONS_TEMPLATES['review_form_project_edit_name'],
                             BUTTONS_TEMPLATES['review_form_project_edit_description']])

            else:
                rows.append([BUTTONS_TEMPLATES['review_form_project_edit_name'],
                             BUTTONS_TEMPLATES['review_form_project_edit_description'],
                             BUTTONS_TEMPLATES['review_form_project_edit_contacts']])
            rows.append([BUTTONS_TEMPLATES['review_form_projects_list']])
            markup = InlineKeyboardBuilder.build(*rows, pk=self.args['model'].id)
            return markup

        elif self.args.get('on_rate'):
            arrow_btns = InlineKeyboardBuilder.build_btns_paginator_arrows(
                BUTTONS_TEMPLATES['coworker_review_projects_choose'],
                left_model=self.args.get('left_project'),
                right_model=self.args.get('right_project'),
            )
            form_btn = InlineKeyboardBuilder.build_btns(BUTTONS_TEMPLATES['coworker_review_form'],
                                                        pk=self.args['model'].form_id)
            markup = InlineKeyboardBuilder.build_list(RatingService().all,
                                                      BUTTONS_TEMPLATES['coworker_review_project_choose_rate'],
                                                      arrow_btns,
                                                      form_btn,
                                                      project_pk=self.args['model'].id
                                                      )
            return markup

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """
        title = '[Проект]'
        text = ''

        if self.args.get('is_name'):
            description = 'Отправьте в сообщении название проекта'

        elif self.args.get('is_description'):
            description = 'Отправьте в сообщении краткое описание проекта и своей роли на нём'

        elif self.args.get('is_contacts'):
            description = 'Отправьте в сообщении логины коллег кто может оценить'

        elif self.args.get('can_edit'):
            description = 'Выберите что вы хотите изменить в проекте'

        elif self.args.get('on_rate'):
            description = 'Оцените проект от 1 🌟 до 5 🌟\n'
            for i, rating in enumerate(RatingService().all):
                description += f'{"🌟" * rating.value} - {rating.name}\n'
            if self.args.get('rating'):
                stars = '🌟' * self.args['rating'].value
                text += f'Ваша оценка: {stars}\n'
            if self.args.get('comment'):
                text += 'Ваш комментарий {comment}\n'.format(comment=self.args['comment'])
        else:
            description = ''
        text += f'{self.args["model"].name} {self.args["model"].description} {self.args["model"].users}'

        message_text = self.message_builder.build_message(title=title,
                                                          description=description,
                                                          text=text,
                                                          )
        return message_text


__all__ = ['ProjectForm']
