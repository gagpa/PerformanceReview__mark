from app.tbot.extensions.template import Template
from app.tbot.storages.buttons import BUTTONS_TEMPLATES
from telebot.types import InlineKeyboardMarkup


class Notification(Template):
    """ Оповещение """

    def create_markup(self) -> InlineKeyboardMarkup:
        view = self.args['view']
        form = self.args['form']
        review = self.args['review']

        if view == 'to_boss':
            to_form = BUTTONS_TEMPLATES['boss_review_to_form'].add(review=form.boss_review.id)
            to_list = BUTTONS_TEMPLATES['boss_review_to_list']
            self.extend_keyboard(False, to_form)
            self.extend_keyboard(True, to_list)
            return self.build()

        elif view == 'to_coworkers':
            to_form = BUTTONS_TEMPLATES['coworkers_review_to_form'].add(review=review.id)
            to_list = BUTTONS_TEMPLATES['coworkers_review_to_list']
            self.extend_keyboard(False, to_form)
            self.extend_keyboard(True, to_list)
            return self.build()

        elif view == 'to_hr':
            to_form = BUTTONS_TEMPLATES['hr_review_to_form'].add(review=review.id)
            to_list = BUTTONS_TEMPLATES['hr_review_to_list']
            self.extend_keyboard(False, to_form)
            self.extend_keyboard(True, to_list)
            return self.build()

    def create_message(self) -> str:
        view = self.args['view']
        form = self.args['form']
        review = self.args['review']
        if view == 'to_boss':
            self.build_message(title='🔔 Оповещение', description=f'Пользователь {form.user.fullname} (@{form.user.username}) - Заполнил анкету')
            return self.MESSAGE
        elif view == 'to_coworkers':
            self.build_message(title='🔔 Оповещение', description=f'Ваш коллега {form.user.fullname} (@{form.user.username}) - Попросил вас оценить его работу')
            return self.MESSAGE
        elif view == 'to_hr':
            self.build_message(title='🔔 Оповещение', description=f'Сотрудник {review.coworker.fullname} (@{review.coworker.username}) - Оценил анкету '
                                                                  f'{review.advice.form.user.fullname} (@{review.advice.form.user.username})')
            return self.MESSAGE
