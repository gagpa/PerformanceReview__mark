from telebot.types import InlineKeyboardMarkup

from app.tbot.extensions.template import Template


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
                               description='\nОтправьте в сообщении свои провалы.',
                               text=f' -  {fail.text}')
            return self.MESSAGE


__all__ = ['FailForm']
