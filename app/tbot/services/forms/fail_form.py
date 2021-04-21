from telebot.types import InlineKeyboardMarkup

from app.tbot.extensions import InlineKeyboardBuilder
from app.tbot.extensions.template import Template
from app.tbot.storages import BUTTONS_TEMPLATES


class FailForm(Template):
    """ Шаблон формы провала """

    def create_markup(self) -> InlineKeyboardMarkup:
        """ Создать клавиатуру """
        pass

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """

        view = self.args.get('view')
        fail = self.args.get('fail')

        if view == 'edit':
            self.build_message(title='▪ Провал',
                               description='\nОтправьте в сообщении свой провал или перечислите их через ;',
                               text=f' -  {fail.text}')
            return self.MESSAGE


__all__ = ['FailForm']
