from app.tbot.middlewares.generals_middlewares import \
    check_permission as general_check_permission,\
    add_user as general_add_user, \
    add_review_period as general_add_review_period, \
    add_form as general_add_form, \
    log_command as general_log_user, \
    log_unknown as general_log_unknown, \
    parse_command


def add_user(bot_instance, message):
    """ Добавить пользователя в сообщение """
    general_add_user(message=message)


def add_review_period(bot_instance, message):
    """ Добавить review преиод в message """
    general_add_review_period(message=message)


def add_form(bot_instance, message):
    """ Добавить форму в сообщение """
    general_add_form(message=message)


def log_user(bot_instance, message):
    """ Логировать сообщения пользователя """
    general_log_user(message=message)


def log_unknown(bot_instance, message):
    """ """
    general_log_unknown(message=message)


def check_permissions(bot_instance, message):
    """"""
    general_check_permission(bot_instance, message)


ORDER_MESSAGE_MIDDLEWARES = \
    [
        log_unknown,
        add_user,
        parse_command,
        check_permissions,
        add_review_period,
        add_form,
        log_user,
    ]


__all__ = ['ORDER_MESSAGE_MIDDLEWARES']
