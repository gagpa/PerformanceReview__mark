from telebot.types import InlineKeyboardMarkup

from app.tbot.extensions import InlineKeyboardBuilder
from app.tbot.extensions.template import Template
from app.tbot.storages import BUTTONS_TEMPLATES


class FailsForm(Template):
    """ Шаблон формы провалов """

    def create_markup(self) -> InlineKeyboardMarkup:
        """ Создать клавиатуру """
        rows = []

        if self.args.get('can_edit') and self.args.get('can_del'):
            rows.append([BUTTONS_TEMPLATES['review_form_fails_add']])
            rows.append([BUTTONS_TEMPLATES['review_form_fails_edit_choose'],
                         BUTTONS_TEMPLATES['review_form_fails_delete_choose']])
            rows.append([BUTTONS_TEMPLATES['review_form']])
            markup = InlineKeyboardBuilder.build(*rows)
            return markup

        elif self.args.get('can_add'):
            rows.append([BUTTONS_TEMPLATES['review_form_fails_add']])
            rows.append([BUTTONS_TEMPLATES['review_form']])
            markup = InlineKeyboardBuilder.build(*rows)
            return markup

        elif self.args.get('can_del'):
            btn = BUTTONS_TEMPLATES['review_form_fail_delete']
            markup = InlineKeyboardBuilder.build_list(self.args['models'], btn)
            return markup

        elif self.args.get('can_edit'):
            btn = BUTTONS_TEMPLATES['review_form_fail_edit']
            markup = InlineKeyboardBuilder.build_list(self.args['models'], btn)
            return markup

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """
        title = '[ПРОВАЛЫ]'

        if self.args.get('can_edit') and self.args.get('can_del'):
            description = 'Факты, которые ты считаешь своими основными провалами, ' \
                          'то, чем вы сами недовольны и что хотели бы исправить и' \
                          ' улучшить в будущем'
            list_data = [f'{self.model.text}' for self.model in self.args['models']]
            message_text = self.message_builder.build_list_message(title=title,
                                                                   description=description,
                                                                   list_data=list_data,
                                                                   )

        elif self.args.get('can_add'):
            description = 'Факты, которые ты считаешь своими основными провалами, ' \
                          'то, чем вы сами недовольны и что хотели бы исправить и' \
                          ' улучшить в будущем'
            text = 'Раздел не заполнен'
            message_text = self.message_builder.build_message(title=title,
                                                              description=description,
                                                              text=text,
                                                              )

        elif self.args.get('can_del'):
            description = 'Выберите провал, которое вы хотите удалить'
            list_data = [f'{self.model.text}' for self.model in self.args['models']]
            message_text = self.message_builder.build_list_message(title=title,
                                                                   description=description,
                                                                   list_data=list_data,
                                                                   )

        elif self.args.get('can_edit'):
            description = 'Выберите провал, которое вы хотите изменить'
            list_data = [f'{self.model.text}' for self.model in self.args['models']]
            message_text = self.message_builder.build_list_message(title=title,
                                                                   description=description,
                                                                   list_data=list_data,
                                                                   )
        elif self.args.get('form'):
            description = ''
            list_data = [f'{self.model.text}' for self.model in self.args['models']]
            message_text = self.message_builder.build_list_message(title=title,
                                                                   description=description,
                                                                   list_data=list_data,
                                                                   )
            return message_text

        else:
            description = 'Отправьте в сообщении свои основные провалы'
            list_data = [f'{self.model.text}' for self.model in self.args['models']]
            message_text = self.message_builder.build_list_message(title=title,
                                                                   description=description,
                                                                   list_data=list_data,
                                                                   )
        return message_text


__all__ = ['FailsForm']
