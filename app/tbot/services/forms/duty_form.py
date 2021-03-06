from typing import Optional

from telebot.types import InlineKeyboardMarkup

from app.tbot.extensions.template import Template


class DutyForm(Template):
    """ Шаблон формы достижений """

    def create_markup(self) -> Optional[InlineKeyboardMarkup]:
        """ Создать клавиатуру """
        pass

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """
        view = self.args.get('view')
        duty = self.args.get('duty')

        if view == 'edit':
            self.build_message(title='▪️Обязанность',
                               description='\n❕ Отправьте в сообщении свои обязанности.',
                               text=f' -  {duty.text}')
            return self.MESSAGE


__all__ = ['DutyForm']
