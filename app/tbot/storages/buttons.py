from telebot.types import InlineKeyboardButton

"""
Файл с кнопками для клавиатур.
"""

BUTTONS = {
    'default': {
        'form': InlineKeyboardButton(text='Анкета', callback_data='form'),
    },
    'form': {
        'duty': InlineKeyboardButton(text='Обязанности', callback_data='duty_form'),
        'projects': InlineKeyboardButton(text='Проекты', callback_data='projects_form'),
        'achievements': InlineKeyboardButton(text='Достижения', callback_data='achievements_form'),
        'fails': InlineKeyboardButton(text='Провалы', callback_data='fails_form'),
        'submit': InlineKeyboardButton(text='Отправить руководителю', callback_data='submit_form'),
    },
    'duty': {
        'add': InlineKeyboardButton(text='Добавить', callback_data='duty_add'),
        'edit': InlineKeyboardButton(text='Изменить', callback_data='duty_edit'),
    },
    'projects': {
        'add': InlineKeyboardButton(text='Добавить', callback_data='project_add'),
    },
    'project': {
        'edit_choose': InlineKeyboardButton(text='Изменить', callback_data='project_edit'),
        'delete_choose': InlineKeyboardButton(text='Удалить', callback_data='project_delete'),
        'delete': InlineKeyboardButton(text='{index}', callback_data='project_delete {pk}'),
        'edit': InlineKeyboardButton(text='{index}', callback_data='project_edit {pk}'),
        'name': InlineKeyboardButton(text='Название', callback_data='project_name {pk}'),
        'description': InlineKeyboardButton(text='Описание', callback_data='project_description {pk}'),
        'contacts': InlineKeyboardButton(text='Контакты', callback_data='project_users {pk}'),
    },
    'achievements': {
        'add': InlineKeyboardButton(text='Добавить', callback_data='achievements_add'),
        'edit_choose': InlineKeyboardButton(text='Изменить', callback_data='achievement_edit'),
        'delete_choose': InlineKeyboardButton(text='Удалить', callback_data='achievement_delete')
    },
    'achievement': {
        'delete': InlineKeyboardButton(text='{index}', callback_data='achievement_delete {pk}'),
        'edit': InlineKeyboardButton(text='{index}', callback_data='achievement_edit {pk}'),
    },
    'fails': {
        'add': InlineKeyboardButton(text='Добавить', callback_data='fails_add'),
        'edit_choose': InlineKeyboardButton(text='Изменить', callback_data='fail_edit'),
        'delete_choose': InlineKeyboardButton(text='Удалить', callback_data='fail_delete')
    },
    'fail': {
        'delete': InlineKeyboardButton(text='{index}', callback_data='fail_delete {pk}'),
        'edit': InlineKeyboardButton(text='{index}', callback_data='fail_edit {pk}'),
    },
}
