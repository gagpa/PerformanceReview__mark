from telebot.types import InlineKeyboardMarkup

from app.tbot.extensions.template import Template


class AuthForm(Template):
    """ Шаблон формы регистрации """

    def create_markup(self) -> InlineKeyboardMarkup:
        """ Создать клавиатуру """
        pass

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """
        title = ''
        text = ''

        if self.args.get('is_name'):
            description = 'Введите свое ФИО'

        elif self.args.get('is_position'):
            description = 'Введите свою должность'

        elif self.args.get('is_department'):
            description = 'Введите свой отдел'

        elif self.args.get('is_boss'):
            description = 'Введите логин руководителя в телеграмм @login или введите "Нет"'

        elif self.args.get('is_end'):
            description = 'Спасибо. Ожидайте разрешения доступа. Вам поступит сообщение.'

        elif self.args.get('is_not_name'):
            description = 'Что-то пошло не так. Введите заново свое ФИО'

        elif self.args.get('is_not_position'):
            description = 'Такой должности не существует. Попробуйте снова'

        elif self.args.get('is_not_department'):
            description = 'Такого отдела не существует. Попробуйте снова'

        else:
            description = ''

        message_text = self.message_builder.build_message(title=title,
                                                          description=description,
                                                          text=text,
                                                          )
        return message_text


__all__ = ['AuthForm']
