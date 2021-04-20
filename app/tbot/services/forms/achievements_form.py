from telebot.types import InlineKeyboardMarkup

from app.tbot.extensions.template import Template
from app.tbot.storages import BUTTONS_TEMPLATES


class AchievementsForm(Template):
    """ Шаблон формы достижений """

    def create_markup(self) -> InlineKeyboardMarkup:
        """ Создать клавиатуру """
        rows = []

        if self.args.get('can_edit') and self.args.get('can_del'):
            rows.append([BUTTONS_TEMPLATES['review_form_achievements_add']])
            rows.append([BUTTONS_TEMPLATES['review_form_achievements_edit_choose'],
                         BUTTONS_TEMPLATES['review_form_achievements_delete_choose']])
            rows.append([BUTTONS_TEMPLATES['review_form']])
            markup = self.markup_builder.build(*rows)
            return markup

        elif self.args.get('can_add'):
            rows.append([BUTTONS_TEMPLATES['review_form_achievements_add']])
            rows.append([BUTTONS_TEMPLATES['review_form']])
            markup = self.markup_builder.build(*rows)
            return markup

        elif self.args.get('can_del'):
            btn = BUTTONS_TEMPLATES['review_form_achievement_delete']
            markup = self.markup_builder.build_list(self.args['models'], btn)
            return markup

        elif self.args.get('can_edit'):
            btn = BUTTONS_TEMPLATES['review_form_achievement_edit']
            markup = self.markup_builder.build_list(self.args['models'], btn)
            return markup

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """
        title = '[ДОСТИЖЕНИЯ]'

        if self.args.get('can_edit') and self.args.get('can_del'):
            description = 'Факты, которые ты считаешь своими основными достижениями и успехами'
            list_data = [f'{self.model.text}' for self.model in self.args['models']]
            message_text = self.message_builder.build_list_message(title=title,
                                                                   description=description,
                                                                   list_data=list_data,
                                                                   )

        elif self.args.get('can_add'):
            description = 'Факты, которые ты считаешь своими основными достижениями и успехами'
            text = 'Раздел не заполнен'
            message_text = self.message_builder.build_message(title=title,
                                                              description=description,
                                                              text=text,
                                                              )
        elif self.args.get('can_del'):
            description = 'Выберите достижение, которое вы хотите удалить'
            list_data = [f'{self.model.text}' for self.model in self.args['models']]
            message_text = self.message_builder.build_list_message(title=title,
                                                                   description=description,
                                                                   list_data=list_data,
                                                                   )

        elif self.args.get('can_edit'):
            description = 'Выберите достижение, которое вы хотите изменить'
            list_data = [f'{self.model.text}' for self.model in self.args['models']]
            message_text = self.message_builder.build_list_message(title=title,
                                                                   description=description,
                                                                   list_data=list_data,
                                                                   )

        else:
            description = 'Отправьте в сообщении свои основные достижения и успехи'
            list_data = [f'{self.model.text}' for self.model in self.args['models']]
            message_text = self.message_builder.build_list_message(title=title,
                                                                   description=description,
                                                                   list_data=list_data,
                                                                   )

        return message_text


__all__ = ['AchievementsForm']
