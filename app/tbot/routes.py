from app.tbot import bot
from app.tbot.resources.review_form_views import controller_form, controller_duty, controller_duty_add, \
    controller_duty_edit, controller_project_add, controller_project_delete, controller_projects, \
    controller_project_edit_choose, controller_project_delete_choose, controller_project_edit, \
    controller_project_edit_name, controller_project_edit_description, controller_project_edit_contacts, \
    controller_achievements, controller_achievements_add, controller_achievements_edit_choose, \
    controller_achievement_edit, controller_achievement_delete, controller_achievements_delete_choose, controller_fails, \
    controller_fail_delete, controller_fails_add, controller_fail_edit, controller_fails_edit_choose, \
    controller_fails_delete_choose
from app.tbot.storages.callback_filters import DUTY_CALLBACKS, INDEX_CALLBACKS, PROJECTS_CALLBACKS, \
    PROJECT_CALLBACKS, ACHIEVEMENTS_CALLBACKS, ACHIEVEMENT_CALLBACKS, FAIL_CALLBACKS, FAILS_CALLBACKS


@bot.message_handler(commands=['start'])
def start(call):
    bot.send_message(chat_id=call.chat.id, text=call.chat.id)


@bot.message_handler(commands=['form'])
def form(call):
    """
    Маршрут формы.
    :return:
    """
    form = call.form
    controller_form(message=call, form=form)


@bot.callback_query_handler(func=INDEX_CALLBACKS['form'])
def form(call):
    """
    Маршрут формы.
    :return:
    """
    form = call.form
    controller_form(message=call.message, form=form)


@bot.callback_query_handler(func=DUTY_CALLBACKS['index'])
def form_duty(call):
    """
    Маршрут формы обязанностей.
    """
    form = call.form
    controller_duty(message=call.message, form=form)


@bot.callback_query_handler(func=DUTY_CALLBACKS['add'])
def form_duty_add(call):
    """
    Муршрут формы добавления обязанностей.
    """
    form = call.form
    controller_duty_add(message=call.message, form=form)


@bot.callback_query_handler(func=DUTY_CALLBACKS['edit'])
def form_duty_edit(call):
    """
    Муршрут формы изменения обязанностей.
    """
    form = call.form
    controller_duty_edit(message=call.message, form=form)


@bot.callback_query_handler(func=PROJECTS_CALLBACKS['index'])
def form_projects(call):
    """
    Маршрут формы Проектов.
    """
    form = call.form
    controller_projects(message=call.message, form=form)


@bot.callback_query_handler(func=PROJECTS_CALLBACKS['add'])
def form_project_add(call):
    """
    Муршрут формы добавления проекта.
    """
    form = call.form
    controller_project_add(message=call.message, form=form)


@bot.callback_query_handler(func=PROJECT_CALLBACKS['edit_choose'])
def form_project_edit_choose(call):
    """
    Муршрут формы изменения проекта.
    """
    form = call.form
    controller_project_edit_choose(message=call.message, form=form)


@bot.callback_query_handler(func=PROJECT_CALLBACKS['edit'])
def form_project_edit(call):
    """
    Муршрут формы изменения проекта.
    """
    form = call.form
    controller_project_edit(call=call, form=form)


@bot.callback_query_handler(func=PROJECT_CALLBACKS['edit_name'])
def form_project_edit_name(call):
    """
    Муршрут формы изменения проекта.
    """
    form = call.form
    controller_project_edit_name(call=call, form=form)


@bot.callback_query_handler(func=PROJECT_CALLBACKS['edit_description'])
def form_project_edit_description(call):
    """
    Муршрут формы изменения проекта.
    """
    form = call.form
    controller_project_edit_description(call=call, form=form)


@bot.callback_query_handler(func=PROJECT_CALLBACKS['edit_contacts'])
def form_project_edit_contacts(call):
    """
    Муршрут формы изменения проекта.
    """
    form = call.form
    controller_project_edit_contacts(call=call, form=form)


@bot.callback_query_handler(func=PROJECT_CALLBACKS['delete_choose'])
def form_project_delete_choose(call):
    """
    Муршрут формы удаления проекта.
    """
    form = call.form
    controller_project_delete_choose(message=call.message, form=form)


@bot.callback_query_handler(func=PROJECT_CALLBACKS['delete'])
def form_project_delete(call):
    """
    Муршрут формы удаления проекта.
    """
    form = call.form
    controller_project_delete(call=call, form=form)


@bot.callback_query_handler(func=ACHIEVEMENTS_CALLBACKS['index'])
def form_achievements(call):
    """
    Маршрут формы достижений.
    """
    form = call.form
    controller_achievements(message=call.message, form=form)


@bot.callback_query_handler(func=ACHIEVEMENTS_CALLBACKS['add'])
def form_achievements_add(call):
    """
    Муршрут формы добавления проекта.
    """
    form = call.form
    controller_achievements_add(message=call.message, form=form)


@bot.callback_query_handler(func=ACHIEVEMENTS_CALLBACKS['edit_choose'])
def form_achievement_edit_choose(call):
    """
    Муршрут формы выбора достижения для изменения.
    """
    form = call.form
    controller_achievements_edit_choose(message=call.message, form=form)


@bot.callback_query_handler(func=ACHIEVEMENT_CALLBACKS['edit'])
def form_achievement_edit(call):
    """
    Муршрут формы выбора достижения для изменения.
    """
    form = call.form
    controller_achievement_edit(call=call, form=form)


@bot.callback_query_handler(func=ACHIEVEMENTS_CALLBACKS['delete_choose'])
def form_achievement_delete_choose(call):
    """
    Муршрут формы выбора достижения для изменения.
    """
    form = call.form
    controller_achievements_delete_choose(message=call.message, form=form)


@bot.callback_query_handler(func=ACHIEVEMENT_CALLBACKS['delete'])
def form_achievement_delete(call):
    """
    Муршрут формы выбора достижения для изменения.
    """
    form = call.form
    controller_achievement_delete(call=call, form=form)


@bot.callback_query_handler(func=FAILS_CALLBACKS['index'])
def form_fails(call):
    """
    Маршрут формы достижений.
    """
    form = call.form
    controller_fails(message=call.message, form=form)


@bot.callback_query_handler(func=FAILS_CALLBACKS['add'])
def form_fails_add(call):
    """
    Муршрут формы добавления проекта.
    """
    form = call.form
    controller_fails_add(message=call.message, form=form)


@bot.callback_query_handler(func=FAILS_CALLBACKS['edit_choose'])
def form_fail_edit_choose(call):
    """
    Муршрут формы выбора достижения для изменения.
    """
    form = call.form
    controller_fails_edit_choose(message=call.message, form=form)


@bot.callback_query_handler(func=FAIL_CALLBACKS['edit'])
def form_fail_edit(call):
    """
    Муршрут формы выбора достижения для изменения.
    """
    form = call.form
    controller_fail_edit(call=call, form=form)


@bot.callback_query_handler(func=FAILS_CALLBACKS['delete_choose'])
def form_fail_delete_choose(call):
    """
    Муршрут формы выбора достижения для изменения.
    """
    form = call.form
    controller_fails_delete_choose(message=call.message, form=form)


@bot.callback_query_handler(func=FAIL_CALLBACKS['delete'])
def form_fail_delete(call):
    """
    Муршрут формы выбора достижения для изменения.
    """
    form = call.form
    controller_fail_delete(call=call, form=form)
