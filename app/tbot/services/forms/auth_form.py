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
            markup = self.markup_builder.build_list_with_buttons(
                self.args['models'], row, departament=self.args.get('departament'))
            return markup
        elif self.args.get('is_department'):
            row = BUTTONS_TEMPLATES['get_department']
            markup = self.markup_builder.build_list_with_buttons(self.args['models'], row)
            return markup
        elif self.args.get('wrong'):
            markup = self.markup_builder.build_reply_keyboard(PERMISSIONS[user.role.name])
            return markup

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """
        title = ''
        text = ''
        description = ''

        if self.args.get('is_name'):
            title = 'Как тебя зовут? Напиши свою Фамилию Имя Отчество'

        elif self.args.get('is_department'):
            title = 'Привет, я бот Марк.\n' \
                    'Я помогу тебе пройти Performance review: обзор эффективности работы сотрудника за определенный период времени. Этот инструмент позволяет  выявить “слабые” и “сильные” места в компании и повысить  эффективность работы организации в целом.' \
                    '\nДавай знакомиться, в каком отделе ты работаешь?'

        elif self.args.get('is_position'):
            title = 'Как называется твоя должность?'

        elif self.args.get('is_boss'):
            name = self.args.get('fullname').split(' ')[1]
            description = f'Очень приятно, {name.capitalize()}! Кто твой руководитель? ' \
                          f'Напиши логин руководителя в формате @login. ' \
                          f'Если у тебя нет руководителя, напиши слово НЕТ'

        elif self.args.get('is_end'):
            description = 'Спасибо. Скоро ты получишь доступ для дальнейшей работы.'

        elif self.args.get('is_not_name'):
            description = 'Что-то пошло не так. Введите заново свое ФИО'

        elif self.args.get('is_not_position'):
            description = 'Такой должности не существует. Попробуйте снова'

        elif self.args.get('is_not_department'):
            description = 'Такого отдела не существует. Попробуйте снова'

        elif self.args.get('exist'):
            description = 'Добро пожаловать!'

        elif self.args.get('no_username'):
            title = 'Пожалуйста, установите логин в Telegram для использования системы.'
            description = 'Для создания ника:' \
                          '\n1) В настройках Telegram перейдите в свой профиль ' \
                          '(в самом верху раздела настройки)' \
                          '\n2) В поле «Имя пользователя» введите придуманный вами ник ' \
                          'и нажмите «Готово»'

        elif self.args.get('wrong'):
            description = 'У вас недостаточно прав.'

        else:
            description = ''

        message_text = self.message_builder.build_message(title=title,
                                                          description=description,
                                                          text=text,
                                                          )
        return message_text


__all__ = ['AuthForm']
