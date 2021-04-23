from typing import Optional

from telebot.types import InlineKeyboardMarkup

from app.tbot.extensions.template import Template
from app.tbot.storages import BUTTONS_TEMPLATES


class UserForm(Template):
    """ Шаблон формы пользователя """

    def create_markup(self) -> Optional[InlineKeyboardMarkup]:
        """ Создать клавиатуру """
        rows = []

        if self.args.get('can_edit'):
            rows.append(
                [BUTTONS_TEMPLATES['request_accept_view'].add(user=self.args.get('model').id),
                 BUTTONS_TEMPLATES['request_delete_view'].add(user=self.args.get('model').id)])
            rows.append([BUTTONS_TEMPLATES['request_view_back']])
            markup = self.markup_builder.build(*rows)
            return markup

        elif self.args.get('can_edit_user'):
            rows.append([BUTTONS_TEMPLATES['user_edit_view'].add(user=self.args.get('model').id),
                         BUTTONS_TEMPLATES['user_delete_view'].add(
                             user=self.args.get('model').id)])
            rows.append([BUTTONS_TEMPLATES['user_view_back']])
            markup = self.markup_builder.build(*rows)
            return markup

        elif self.args.get('models') and self.args.get('requests'):
            row = BUTTONS_TEMPLATES['request_view']
            markup = self.markup_builder.build_list(self.args['models'], row)
            return markup

        elif self.args.get('models') and self.args.get('users_list'):
            row = BUTTONS_TEMPLATES['user_view']
            markup = self.markup_builder.build_list(self.args['models'], row)
            return markup

        elif self.args.get('edit_step'):
            rows.append([BUTTONS_TEMPLATES['user_edit_fullname'],
                         BUTTONS_TEMPLATES['user_edit_boss']])
            rows.append([BUTTONS_TEMPLATES['user_edit_position'],
                         BUTTONS_TEMPLATES['user_edit_department'],
                         BUTTONS_TEMPLATES['user_edit_role']])
            rows.append([BUTTONS_TEMPLATES['back_to_user'].add(pk=self.args.get('model').id)])
            markup = self.markup_builder.build(*rows, user=self.args.get('model').id)
            return markup
        elif self.args.get('confirm') and self.args.get('request'):
            rows.append([BUTTONS_TEMPLATES['request_delete'],
                         BUTTONS_TEMPLATES['cancel_deletion']])
            markup = self.markup_builder.build(*rows, user=self.args.get('model').id)
            return markup
        elif self.args.get('confirm') and self.args.get('user'):
            rows.append([BUTTONS_TEMPLATES['user_delete'],
                         BUTTONS_TEMPLATES['cancel_user_delete']])
            markup = self.markup_builder.build(*rows, user=self.args.get('model').id)
            return markup
        elif self.args.get('edit_position_step'):
            row = BUTTONS_TEMPLATES['edit_position']
            markup = self.markup_builder.build_list(self.args['positions'], row,
                                                    user_id=self.args.get('user_id'))
            return markup
        elif self.args.get('edit_department_step'):
            row = BUTTONS_TEMPLATES['edit_department']
            markup = self.markup_builder.build_list(self.args['departments'], row,
                                                    user_id=self.args.get('user_id'))
            return markup
        elif self.args.get('edit_role_step'):
            row = BUTTONS_TEMPLATES['edit_role']
            markup = self.markup_builder.build_list(self.args['roles'], row,
                                                    user_id=self.args.get('user_id'))
            return markup

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """
        title = ''
        description = ''

        if self.args.get('models') and self.args.get('requests'):
            title = 'Здесь отображаются все входящие запросы'
            list_data = [f'{model.username} - {model.fullname}' for model in self.args["models"]]
            message_text = self.message_builder.build_list_message(title=title,
                                                                   description=description,
                                                                   list_data=list_data,
                                                                   )
        elif self.args.get('models') and self.args.get('users_list'):
            title = 'Здесь отображаются все пользователи'
            list_data = [f'{model.username} - {model.fullname}' for model in self.args["models"]]
            message_text = self.message_builder.build_list_message(title=title,
                                                                   description=description,
                                                                   list_data=list_data,
                                                                   )
        elif self.args.get('can_edit') or self.args.get('can_edit_user'):
            title = 'Информация о пользователе'
            user = self.args["model"]
            text = f'Логин: {user.username}\nФИО: {user.fullname}' \
                   f'\nДолжность: {user.position.name}' \
                   f'\nОтдел: {user.department.name}' \
                   f'\nРуководитель: {user.boss.username if user.boss else "Нет"}' \
                   f'\nРоль: {user.role.name}'
            message_text = self.message_builder.build_message(title=title,
                                                              description=description,
                                                              text=text,
                                                              )
        elif self.args.get('edit_step'):
            text = 'Выберите данные для редактирования'
            message_text = self.message_builder.build_message(title=title,
                                                              description=description,
                                                              text=text,
                                                              )
        elif self.args.get('edit_fullname_step'):
            text = 'Введите новое ФИО:'
            message_text = self.message_builder.build_message(title=title,
                                                              description=description,
                                                              text=text,
                                                              )
        elif self.args.get('edit_role_step'):
            title = 'Введите новую роль:'
            list_data = [model.name for model in self.args.get('roles')]
            message_text = self.message_builder.build_list_message(title=title,
                                                                   description=description,
                                                                   list_data=list_data,
                                                                   )
        elif self.args.get('edit_position_step'):
            title = 'Введите новую должность:'
            list_data = [model.name for model in self.args.get('positions')]
            message_text = self.message_builder.build_list_message(title=title,
                                                                   description=description,
                                                                   list_data=list_data,
                                                                   )
        elif self.args.get('edit_boss_step'):
            text = 'Введите логин нового руководителя:'
            message_text = self.message_builder.build_message(title=title,
                                                              description=description,
                                                              text=text,
                                                              )
        elif self.args.get('edit_department_step'):
            title = 'Введите новый отдел:'
            list_data = [model.name for model in self.args.get('departments')]
            message_text = self.message_builder.build_list_message(title=title,
                                                                   description=description,
                                                                   list_data=list_data,
                                                                   )
        elif self.args.get('changed'):
            text = 'Данные изменены.'
            message_text = self.message_builder.build_message(title=title,
                                                              description=description,
                                                              text=text,
                                                              )
        elif self.args.get('confirm'):
            text = f'Удалить {self.args.get("model").username}?'
            message_text = self.message_builder.build_message(title=title,
                                                              description=description,
                                                              text=text,
                                                              )
        else:
            message_text = self.message_builder.build_message('', '', 'Нет входящих запросов')

        return message_text


__all__ = ['UserForm']
