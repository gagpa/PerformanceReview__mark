from app.tbot.middlewares.generals_middlewares import \
    add_user as general_add_user, \
    add_review_period as general_add_review_period, \
    add_form as general_add_form, \
    log_callback as general_log_user, \
    log_bot as general_log_bot, \
    log_unknown as general_log_unknown, \
    parse_url


def add_user(bot_instance, call):
    """ Добавить пользователя в сообщение """
    general_add_user(message=call.message)


def add_review_period(bot_instance, call):
    """ Добавить review преиод в message """
    general_add_review_period(message=call.message)


def add_form(bot_instance, call):
    """ Добавить форму в сообщение """
    general_add_form(message=call.message)


def log_user(bot_instance, call):
    """ Логировать сообщения пользователя """
    general_log_user(call=call)


def log_unknown_user(bot_instance, call):
    """ """
    general_log_unknown(call.message)


def log_bot(bot_instance, call):
    """ Логировать ответы бота """
    general_log_bot(message=call.message)


ORDER_CALLBACK_QUERY_MIDDLEWARES = \
    [
        add_user,
        parse_url,
        add_review_period,
        add_form,
        log_user
    ]


__all__ = ['ORDER_CALLBACK_QUERY_MIDDLEWARES']
