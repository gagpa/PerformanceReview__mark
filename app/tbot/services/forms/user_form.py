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
            users = self.args.get('models')
            page = self.args.get('page')
            count_obj = len(users)
            users = self.cut_per_page(users, page)
            unique_args = [{'pk': user.id} for user in users]
            main_template = BUTTONS_TEMPLATES['user_view']
            pagination_template = BUTTONS_TEMPLATES['user_list_view']
            self.add_paginator(paginator=pagination_template, page=page, count_obj=count_obj)
            return self.build_list(main_template, unique_args)

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
            rows.append(self.markup_builder.build_btns(BUTTONS_TEMPLATES['back_to_edit'],
                                                       user=self.args.get('user_id')))
            markup = self.markup_builder.build_list_with_buttons(self.args['positions'], row, 2,
                                                                 *rows,
                                                                 user_id=self.args.get('user_id'))
            return markup
        elif self.args.get('edit_department_step'):
            row = BUTTONS_TEMPLATES['edit_department']
            rows.append(self.markup_builder.build_btns(BUTTONS_TEMPLATES['back_to_edit'],
                                                       user=self.args.get('user_id')))
            markup = self.markup_builder.build_list_with_buttons(self.args['departments'], row, 2,
                                                                 *rows,
                                                                 user_id=self.args.get('user_id'))
            return markup
        elif self.args.get('edit_role_step'):
            row = BUTTONS_TEMPLATES['edit_role']
            rows.append(self.markup_builder.build_btns(BUTTONS_TEMPLATES['back_to_edit'],
                                                       user=self.args.get('user_id')))
            markup = self.markup_builder.build_list_with_buttons(self.args['roles'], row, 2, *rows,
                                                                 user_id=self.args.get('user_id'))
            return markup

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """
        title = ''
        description = ''
        users = self.args.get('models')
        page = self.args.get('page')
        if page:
            users = self.cut_per_page(users, page) if users else None

        if self.args.get('models') and self.args.get('requests'):
            title = 'Здесь отображаются все входящие запросы'
            list_data = [f'{model.username} - {model.fullname}' for model in self.args["models"]]
            message_text = self.message_builder.build_list_message(title=title,
                                                                   description=description,
                                                                   list_data=list_data,
                                                                   )
        elif users and self.args.get('users_list'):
            title = 'Здесь отображаются все пользователи'
            list_data = [f'{user.username} - {user.fullname}' for user in users]
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
            text = '❕ Выберите новую роль:'
            message_text = self.message_builder.build_message(title=title,
                                                              description=description,
                                                              text=text,
                                                              )
        elif self.args.get('edit_position_step'):
            text = '❕ Выберите новую должность:'
            message_text = self.message_builder.build_message(title=title,
                                                              description=description,
                                                              text=text,
                                                              )
        elif self.args.get('edit_boss_step'):
            text = 'Введите логин нового руководителя:'
            message_text = self.message_builder.build_message(title=title,
                                                              description=description,
                                                              text=text,
                                                              )
        elif self.args.get('edit_department_step'):
            text = 'Введите новый отдел:'
            message_text = self.message_builder.build_message(title=title,
                                                              description=description,
                                                              text=text,
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
