from telebot.types import InlineKeyboardMarkup

from app.tbot.extensions import InlineKeyboardBuilder
from app.tbot.extensions.template import Template
from app.tbot.storages import BUTTONS_TEMPLATES


class ProjectsForm(Template):
    """ Шаблон формы проектов """

    def create_markup(self) -> InlineKeyboardMarkup:
        """ Создать клавиатуру """
        rows = []

        if self.args.get('can_edit') and self.args.get('can_del'):
            rows.append([BUTTONS_TEMPLATES['review_form_project_add']])
            rows.append([BUTTONS_TEMPLATES['review_form_project_edit_choose'],
                         BUTTONS_TEMPLATES['review_form_project_delete_choose']])
            rows.append([BUTTONS_TEMPLATES['review_form']])
            markup = InlineKeyboardBuilder.build(*rows)
            return markup

        elif self.args.get('can_add'):
            rows.append([BUTTONS_TEMPLATES['review_form_project_add']])
            rows.append([BUTTONS_TEMPLATES['review_form']])
            markup = InlineKeyboardBuilder.build(*rows)
            return markup

        elif self.args.get('can_del'):
            btn = BUTTONS_TEMPLATES['review_form_project_delete']
            markup = self.markup_builder.build_list(self.args['models'], btn)
            return markup

        elif self.args.get('can_edit'):
            btn = BUTTONS_TEMPLATES['review_form_project_edit']
            markup = self.markup_builder.build_list(self.args['models'], btn)
            return markup

        elif self.args.get('on_coworker_review'):
            btn = BUTTONS_TEMPLATES['coworker_review_projects_choose']
            markup = self.markup_builder.build_list(self.args['models'], btn)
            return markup

        elif self.args.get('on_hr_review'):
            args = {'advice': self.args['advice'], 'form': self.args['form'].id, 'coworker': self.args['coworker'].id}
            btns = self.markup_builder.build_btns(BUTTONS_TEMPLATES['hr_review_back_to_decline'],
                                                  **args)
            markup = self.markup_builder.build_list_up(BUTTONS_TEMPLATES['hr_review_comment_rating'],
                                                       [{'project': project.id} for project in
                                                        self.args['projects']],
                                                       {'cw': self.args['coworker'].id,
                                                        'f': self.args['form'].id,
                                                        'adv': self.args['advice']},
                                                       btns
                                                       )
            return markup

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """

        title = 'Проекты'

        if self.args.get('on_hr_review'):
            description = 'Выберите комментарий сотрудника'
            list_data = []
            for project, rating in zip(self.args['projects'], self.args['ratings']):
                project_text = f'____________\nНазвание - {project.name}\n' \
                               f'Описание - {project.description}\n'

                rating_text = self.message_builder.build_message(title='Комментарий и Оценка коллеги',
                                                                 description='',
                                                                 text=f'Оценка: {rating.rating.value} - {rating.text}')
                if rating.hr_comment:
                    text = f'{rating.hr_comment.text}'
                else:
                    text = f'Без комментария'

                hr_text = self.message_builder.build_message(title='Комментарий HR',
                                                             description='',
                                                             text=text)

                list_data.append(f'{project_text}▫ {rating_text}\n▫ {hr_text}')
            message_text = self.message_builder.build_list_message(title=title,
                                                                   description=description,
                                                                   list_data=list_data,
                                                                   )
            return message_text
        elif self.args.get('form'):
            description = '***'
            list_data = [f'{model.name}\n{model.description} {model.users}' for model in self.args['models']]
            message_text = self.message_builder.build_list_message(title=title,
                                                                   description=description,
                                                                   list_data=list_data,
                                                                   )
            return message_text

        else:
            if self.args.get('models'):
                description = 'Перечислите проекты, которые ты выполнял или измените данные'
                list_data = [f'{model.name}\n{model.description} {model.users}' for model in self.args['models']]
            else:
                description = 'Перечислите проекты, которые ты выполнял'
                list_data = None

        message_text = self.message_builder.build_list_message(title=title,
                                                               description=description,
                                                               list_data=list_data,
                                                               )
        return message_text


__all__ = ['ProjectsForm']
