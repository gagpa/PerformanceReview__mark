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
            markup = InlineKeyboardBuilder.build_list(self.args['models'], btn)
            return markup

        elif self.args.get('can_edit'):
            btn = BUTTONS_TEMPLATES['review_form_project_edit']
            markup = InlineKeyboardBuilder.build_list(self.args['models'], btn)
            return markup

        elif self.args.get('on_coworker_review'):
            btn = BUTTONS_TEMPLATES['coworker_review_projects_choose']
            markup = InlineKeyboardBuilder.build_list(self.args['models'], btn)
            return markup

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """

        title = '[ПРОЕКТЫ]'

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
