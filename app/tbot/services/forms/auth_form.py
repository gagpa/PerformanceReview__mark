from telebot.types import InlineKeyboardMarkup

from app.tbot.extensions.template import Template
from app.tbot.storages import BUTTONS_TEMPLATES
from app.tbot.storages.permissions import PERMISSIONS


class AuthForm(Template):
    """ Шаблон формы регистрации """

    def create_markup(self) -> InlineKeyboardMarkup:
        """ Создать клавиатуру """
        user = self.args.get('user')
        if self.args.get('is_position'):
            row = BUTTONS_TEMPLATES['get_position']
            markup = self.markup_builder.build_list(self.args['models'], row)
            return markup
        elif self.args.get('is_department'):
            row = BUTTONS_TEMPLATES['get_department']
            markup = self.markup_builder.build_list(self.args['models'], row,
                                                    position=self.args.get('position'))
            return markup
        elif self.args.get('wrong'):
            markup = self.markup_builder.build_reply_keyboard(PERMISSIONS[user.role.name])
            return markup

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """
        title = ''
        text = ''

        if self.args.get('is_name'):
            description = 'Введите свое ФИО'

        elif self.args.get('is_position'):
            description = 'Привет, я бот Марк.\n' \
                          'Я помогу тебе пройти Performance review: обзор эффективности работы сотрудника за определенный период времени. Этот инструмент позволяет  выявить “слабые” и “сильные” места в компании и повысить  эффективность работы организации в целом.' \
                          '\nДавай знакомиться, в каком отделе ты работаешь?' \
                          '\n❕ Выберите свою должность:'
            list_data = [model.name for model in self.args.get('models')]

        elif self.args.get('is_department'):
            description = '\n❕ Выберите свой отдел:'
            list_data = [model.name for model in self.args.get('models')]

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

        elif self.args.get('exist'):
            description = 'Добро пожаловать!'

        elif self.args.get('no_username'):
            description = 'Пожалуйста, установите логин в Telegram для использования системы.'

        elif self.args.get('wrong'):
            description = 'У вас недостаточно прав.'

        else:
            description = ''

        if self.args.get('is_position') or self.args.get('is_department'):
            message_text = self.message_builder.build_list_message(title=title,
                                                                   description=description,
                                                                   list_data=list_data,
                                                                   )
        else:
            message_text = self.message_builder.build_message(title=title,
                                                              description=description,
                                                              text=text,
                                                              )
        return message_text


__all__ = ['AuthForm']
