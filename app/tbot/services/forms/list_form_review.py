from telebot.types import InlineKeyboardMarkup

from app.tbot.extensions.template import Template
from app.tbot.storages import BUTTONS_TEMPLATES


class ListFormReview(Template):
    """ Шаблон списка анкет на проверку """

    def create_markup(self) -> InlineKeyboardMarkup:
        """ Создать клавиатуру """
        if self.args.get('on_boss_review'):
            return self.markup_builder.build_list(self.args['models'], BUTTONS_TEMPLATES['boss_review_form'])

        elif self.args.get('on_coworker_review'):
            return self.markup_builder.build_list(self.args['models'], BUTTONS_TEMPLATES['coworker_review_form'])

        elif self.args.get('on_hr_review'):
            unique_args = [{'advice': advice.id, 'form': advice.form.id} for advice in self.args['advices']]
            return self.markup_builder.build_list_up(BUTTONS_TEMPLATES['hr_review_form'], unique_args=unique_args)

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """
        title = '[СПИСОК АНКЕТ НА ПРОВЕРКУ]'

        if self.args.get('on_boss_review'):
            description = 'Можете выбрать форму подчинённого на проверку.'
            list_data = [f'{self.model.user.fullname}' for self.model in self.args['models']]
            return self.message_builder.build_list_message(title=title,
                                                           description=description,
                                                           list_data=list_data)

        elif self.args.get('on_coworker_review'):
            description = 'Можете выбрать форму коллеги на оценку.'
            list_data = [f'{self.model.coworker.fullname}' for self.model in self.args['models']]
            return self.message_builder.build_list_message(title=title,
                                                           description=description,
                                                           list_data=list_data)

        elif self.args.get('on_hr_review'):
            description = 'Можете выбрать форму на проверку.'
            list_data = [f'{advice.coworker.fullname} - {advice.form.user.username}' for advice in self.args['advices']]
            return self.message_builder.build_list_message(title=title,
                                                           description=description,
                                                           list_data=list_data)


__all__ = ['ListFormReview']
