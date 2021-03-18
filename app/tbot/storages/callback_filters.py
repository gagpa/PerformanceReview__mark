from app.tbot.storages.buttons import BUTTONS

DUTY_CALLBACKS = {
    'index': lambda call: call.data == BUTTONS['form']['duty'].callback_data,
    'add': lambda call: call.data == BUTTONS['duty']['add'].callback_data,
    'edit': lambda call: call.data == BUTTONS['duty']['edit'].callback_data,
}

INDEX_CALLBACKS = {
    'form': lambda call: call.data == BUTTONS['default']['form'].callback_data,
}

PROJECTS_CALLBACKS = {
    'index': lambda call: call.data == BUTTONS['form']['projects'].callback_data,
    'add': lambda call: call.data == BUTTONS['projects']['add'].callback_data,
}

PROJECT_CALLBACKS = {
    'edit_choose': lambda call: call.data == BUTTONS['project']['edit_choose'].callback_data,
    'delete_choose': lambda call: call.data == BUTTONS['project']['delete_choose'].callback_data,
    'delete': lambda call: call.data.split(' ')[-1].isdigit() and call.data.split(' ')[0] in str(
        BUTTONS['project']['delete'].callback_data),
    'edit': lambda call: call.data.split(' ')[-1].isdigit() and call.data.split(' ')[0] in str(
        BUTTONS['project']['edit'].callback_data),
    'edit_name': lambda call: call.data.split(' ')[-1].isdigit() and call.data.split(' ')[0] in str(
        BUTTONS['project']['name'].callback_data),
    'edit_description': lambda call: call.data.split(' ')[-1].isdigit() and call.data.split(' ')[0] in str(
        BUTTONS['project']['description'].callback_data),
    'edit_contacts': lambda call: call.data.split(' ')[-1].isdigit() and call.data.split(' ')[0] in str(
        BUTTONS['project']['contacts'].callback_data),
}

ACHIEVEMENTS_CALLBACKS = {
    'index': lambda call: call.data == BUTTONS['form']['achievements'].callback_data,
    'add': lambda call: call.data == BUTTONS['achievements']['add'].callback_data,
    'edit_choose': lambda call: call.data == BUTTONS['achievements']['edit_choose'].callback_data,
    'delete_choose': lambda call: call.data == BUTTONS['achievements']['delete_choose'].callback_data,
}

ACHIEVEMENT_CALLBACKS = {
    'delete': lambda call: call.data.split(' ')[-1].isdigit() and call.data.split(' ')[0] in str(
        BUTTONS['achievement']['delete'].callback_data),
    'edit': lambda call: call.data.split(' ')[-1].isdigit() and call.data.split(' ')[0] in str(
        BUTTONS['achievement']['edit'].callback_data),
}


FAILS_CALLBACKS = {
    'index': lambda call: call.data == BUTTONS['form']['fails'].callback_data,
    'add': lambda call: call.data == BUTTONS['fails']['add'].callback_data,
    'edit_choose': lambda call: call.data == BUTTONS['fails']['edit_choose'].callback_data,
    'delete_choose': lambda call: call.data == BUTTONS['fails']['delete_choose'].callback_data,
}

FAIL_CALLBACKS = {
    'delete': lambda call: call.data.split(' ')[-1].isdigit() and call.data.split(' ')[0] in str(
        BUTTONS['fail']['delete'].callback_data),
    'edit': lambda call: call.data.split(' ')[-1].isdigit() and call.data.split(' ')[0] in str(
        BUTTONS['fail']['edit'].callback_data),
}
