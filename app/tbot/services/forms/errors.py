from telebot.types import InlineKeyboardMarkup

from app.tbot.extensions.template import Template


class ReviewIsNotUpped(Template):

    def create_markup(self) -> InlineKeyboardMarkup:
        pass

    def create_message(self) -> str:
        self.build_message(title='Ревью завершено',
                           description='На данный момент вы не можете воспользоваться данным функционалом.\n'
                                       'В след. раз будьте более оперативным',
                           )
        return self.MESSAGE
