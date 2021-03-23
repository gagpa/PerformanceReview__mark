from typing import List, Optional, Tuple

from telebot.types import InlineKeyboardMarkup

from app.models import Achievement
from app.tbot.extensions import InlineKeyboardBuilder
from app.tbot.extensions import MessageBuilder
from app.tbot.services.forms.achievement_form import AchievementForm
from app.tbot.storages import BUTTONS_TEMPLATES


class AchievementsForm:
    """ Шаблон формы достижений """
    __message_builder = MessageBuilder()
    markup = None
    templates = []
    models = []

    def __init__(self, models: List[Achievement] = None,
                 can_add: bool = False,
                 can_edit: bool = False,
                 can_del: bool = False,
                 ):

        self.can_add = can_add
        self.can_edit = can_edit
        self.can_del = can_del

        if models:
            self.add(models)

    def add(self, data: List[Achievement]):
        """ Добавить достижения в форму """
        self.models = data
        for achievement in self.models:
            self.templates.append(AchievementForm(achievement))

    def __create_markup(self) -> Optional[InlineKeyboardMarkup]:
        """ Создать клавиатуру """
        rows = []
        if self.can_edit and self.can_del:
            row = [BUTTONS_TEMPLATES['achievements_add']]
            rows.append(row)
            row = [BUTTONS_TEMPLATES['achievements_edit_choose'], BUTTONS_TEMPLATES['achievements_delete_choose']]
            rows.append(row)
            row = [BUTTONS_TEMPLATES['form']]
            rows.append(row)
            self.markup = InlineKeyboardBuilder.build(*rows)
        elif self.can_add:
            row = [BUTTONS_TEMPLATES['achievements_add']]
            rows.append(row)
            row = [BUTTONS_TEMPLATES['form']]
            rows.append(row)
            self.markup = InlineKeyboardBuilder.build(*rows)
        elif self.can_del:
            btn = BUTTONS_TEMPLATES['achievement_delete']
            self.markup = InlineKeyboardBuilder.build_list(self.models, btn)
        elif self.can_edit:
            btn = BUTTONS_TEMPLATES['achievement_edit']
            self.markup = InlineKeyboardBuilder.build_list(self.models, btn)
        return self.markup

    def __create_message_text(self) -> str:
        """ Вернуть преобразованное сообщение """
        title = '[ДОСТИЖЕНИЯ]'
        if self.can_edit and self.can_del:
            description = 'Факты, которые ты считаешь своими основными достижениями и успехами'
            list_data = [f'{self.model.text}' for self.model in self.models]
            message_text = self.__message_builder.build_list_message(title=title,
                                                                     description=description,
                                                                     list_data=list_data,
                                                                     )
        elif self.can_add:
            description = 'Факты, которые ты считаешь своими основными достижениями и успехами'
            text = 'Раздел не заполнен'
            message_text = self.__message_builder.build_message(title=title,
                                                                description=description,
                                                                text=text,
                                                                )
        elif self.can_del:
            description = 'Выберите достижение, которое вы хотите удалить'
            list_data = [f'{self.model.text}' for self.model in self.models]
            message_text = self.__message_builder.build_list_message(title=title,
                                                                     description=description,
                                                                     list_data=list_data,
                                                                     )
        elif self.can_edit:
            description = 'Выберите достижение, которое вы хотите изменить'
            list_data = [f'{self.model.text}' for self.model in self.models]
            message_text = self.__message_builder.build_list_message(title=title,
                                                                     description=description,
                                                                     list_data=list_data,
                                                                     )
        else:
            description = 'Отправьте в сообщении свои основные достижения и успехи'
            list_data = [f'{self.model.text}' for self.model in self.models]
            message_text = self.__message_builder.build_list_message(title=title,
                                                                     description=description,
                                                                     list_data=list_data,
                                                                     )
        return message_text

    def dump(self) -> Tuple[str, Optional[InlineKeyboardMarkup]]:
        """ Вернуть преобразованное данные """
        message_text = self.__create_message_text()
        markup = self.__create_markup()
        return message_text, markup


__all__ = ['AchievementsForm']
