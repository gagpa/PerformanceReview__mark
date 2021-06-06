from typing import Optional

from telebot.types import InlineKeyboardMarkup

from app.tbot.extensions.template import Template


class CoworkerAdviceForm(Template):
    """ Шаблон формы совета """

    def create_markup(self) -> Optional[InlineKeyboardMarkup]:
        """ Создать клавиатуру """
        pass

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """
        view = self.args.get('view')
        coworker_advice = self.args.get('coworker_advice')

        if view == 'edit':
            self.build_message(title='▪️Совет',
                               description='\n❕ Отправьте в сообщении свой совет.',
                               text=f'{coworker_advice.text}')
            return self.MESSAGE
        elif view == 'hr':
            self.build_message(title='▪️Совет',
                               description='\n❕ Отправьте в сообщении, что нужно исправить или "+" чтобы убрать свой комментарий.',
                               text=f'{coworker_advice.text}')
            return self.MESSAGE


__all__ = ['CoworkerAdviceForm']
