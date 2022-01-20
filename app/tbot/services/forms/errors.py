from telebot.types import InlineKeyboardMarkup

from app.tbot.extensions.template import Template


class ReviewIsNotUpped(Template):

    def create_markup(self) -> InlineKeyboardMarkup:
        pass

    def create_message(self) -> str:
        self.build_message(title='Ревью завершено',
                           description='Ревью завершено. Вы уже не можете воспользоваться данным функционалом.',
                           )
        return self.MESSAGE
