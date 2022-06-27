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
            for position in self.args['models']:
                btn = BUTTONS_TEMPLATES['get_position']
                btn.add(pk=position.id, departament=self.args['departament'])
                btn.text = position.name
                self.extend_keyboard(False, btn)
            self.extend_keyboard(True, BUTTONS_TEMPLATES['get_reg'])
            return self.build()

        elif self.args.get('is_department'):
            unique_args = [{'pk': department.id} for department in self.args['models']]
            return self.build_list(BUTTONS_TEMPLATES['get_department'], unique_args=unique_args)
        elif self.args.get('wrong'):
            markup = self.markup_builder.build_reply_keyboard(PERMISSIONS[user.role.name])
            return markup

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """
        title = '📝 Твой профиль'
        text = ''
        description = ''

        if self.args.get('is_name'):
            description = '❕ Как тебя зовут? Напиши свою Фамилию Имя Отчество:'

        elif self.args.get('is_department'):
            departments = '\n'.join([f'{i + 1}. {department.name}' for i, department in enumerate(self.args['models'])])
            description = 'Привет, я бот Марк.\n\n' \
                          'Я помогу тебе пройти Performance review: обзор эффективности работы сотрудника за определенный период времени. Этот инструмент позволяет  выявить “слабые” и “сильные” места в компании и повысить  эффективность работы организации в целом.' \
                          '\n\n❕ Давай знакомиться, в какой дирекции ты работаешь?\n\n' \
                          'Дирекции:\n' \
                          f'{departments}'

        elif self.args.get('is_position'):
            description = '❕ Как называется твоя должность?'

        elif self.args.get('is_boss'):
            try:
                name = self.args.get('fullname').split(' ')[1]
            except IndexError:
                name = self.args.get('fullname')
            description = f'Очень приятно, {name.capitalize()}! Кто твой руководитель?\n' \
                          f'❕ Напиши логин руководителя в формате @login. ' \
                          f'Если у тебя нет руководителя, напиши слово НЕТ'

        elif self.args.get('is_end'):
            description = '❕ Спасибо. Скоро ты получишь доступ для дальнейшей работы.'

        elif self.args.get('is_not_name'):
            description = '❕ Что-то пошло не так. Введите заново свое ФИО:'

        elif self.args.get('is_not_position'):
            description = '❕ Такой должности не существует. Попробуйте снова:'

        elif self.args.get('is_not_department'):
            description = '❕ Такого отдела не существует. Попробуйте снова:'

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
            description = '❕ Выберите раздел.'

        else:
            description = ''

        message_text = self.message_builder.build_message(title=title,
                                                          description=description,
                                                          text=text,
                                                          )
        return message_text


__all__ = ['AuthForm']
