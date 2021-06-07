from telebot.types import InlineKeyboardMarkup

from app.tbot.extensions.template import Template
from app.tbot.storages.buttons import BUTTONS_TEMPLATES
from app.tbot.storages.permissions import PERMISSIONS


class Notification(Template):
    """ Оповещение """

    def create_markup(self) -> InlineKeyboardMarkup:
        view = self.args.get('view')
        form = self.args.get('form')
        review = self.args.get('review')
        role = self.args.get('role')
        user = self.args.get('user')

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

        elif view in {'to_employee', 'start_review'}:
            to_form = BUTTONS_TEMPLATES['review_to_form'].add(review=review.id)
            self.extend_keyboard(False, to_form)
            return self.build()

        elif view == 'copy_last_form':
            last_form = self.args.get('last_form')
            to_form = BUTTONS_TEMPLATES['copy_last_form'].add(last_form=last_form.id)
            self.extend_keyboard(False, to_form)
            return self.build()

        elif view == 'from_hr_to_coworker':
            to_form = BUTTONS_TEMPLATES['coworkers_review_to_form'].add(review=review.id)
            to_list = BUTTONS_TEMPLATES['coworkers_review_to_list']
            self.extend_keyboard(False, to_form)
            self.extend_keyboard(True, to_list)
            return self.build()

        elif view == 'change_role':
            return self.markup_builder.build_reply_keyboard(PERMISSIONS[role])

        elif view == 'request_for_hr':
            to_request = BUTTONS_TEMPLATES['to_request'].add(pk=user.id)
            self.extend_keyboard(False, to_request)
            return self.build()

        elif view == 'add_role':
            return self.markup_builder.build_reply_keyboard(PERMISSIONS[role])

    def create_message(self) -> str:
        view = self.args.get('view')
        form = self.args.get('form')
        review = self.args.get('review')

        if view == 'to_boss':
            description = f'Твой сотрудник {form.user.fullname} (@{form.user.username}) заполнил анкету.' \
                          f'Проверь правильность и напиши свои комментарии, ' \
                          f'если ты считаешь, что анкету нужно дополнить или исправить, ' \
                          f'прежде чем отправлять коллегам на оценку.'
            self.build_message(title='🔔 Оповещение',
                               description=description)
            return self.MESSAGE

        elif view == 'to_coworkers':
            description = f'Ваш коллега {form.user.fullname} (@{form.user.username}) попросил вас оценить его работу'
            self.build_message(title='🔔 Оповещение',
                               description=description)
            return self.MESSAGE

        elif view == 'to_hr':
            description = f'Сотрудник {review.coworker.fullname} (@{review.coworker.username}) оценил анкету ' \
                          f'{review.form.user.fullname} (@{review.form.user.username})'
            self.build_message(title='🔔 Оповещение', description=description)
            return self.MESSAGE

        elif view == 'to_employee':
            description = f'Ваш руководитель {review.boss.fullname} (@{review.boss.username}) ' \
                          f'вернул вам анкету для исправления ошибок'
            self.build_message(title='🔔 Оповещение', description=description)
            return self.MESSAGE
        elif view == 'declined':
            self.build_message(title='🔔 Отправлено на доработку')
            return self.MESSAGE
        elif view == 'start_review':
            description = f"Необходимо заполнить анкету в разделе 'Моя анкета' до {self.args.get('date')}"
            self.build_message(title='🔔 Оповещение', description=description)
            return self.MESSAGE

        elif view == 'from_hr_to_coworker':
            description = f'HR просит вас отредактировать ваши оценки'
            self.build_message(title='🔔 Оповещение', description=description)
            return self.MESSAGE

        elif view == 'accept_to_hr':
            description = f'Форма пользователя {review.advice.form.user.fullname} (@{review.advice.form.user.username})' \
                          f'полностью заполнена'
            self.build_message(title='🔔 Оповещение', description=description)
            return self.MESSAGE

        elif view == 'add_role':
            self.build_message(title='🔔 Оповещение',
                               description='Добро пожаловать. Давай начнем работу.')
            return self.MESSAGE

        elif view == 'change_role':
            self.build_message(title='🔔 Оповещение', description='Вам поменяли роль')
            return self.MESSAGE

        elif view == 'request_for_hr':
            self.build_message(title='🔔 Оповещение',
                               description='Новый запрос на доступ к системе')
            return self.MESSAGE

        elif view == 'copy_last_form':
            self.build_message(title='🔔 Оповещение',
                               description='В предыдущем ревью обнаружена ваша анкета. '
                                           'Скопировать её для нового ревью? '
                                           'Её можно будет отредактировать.')
            return self.MESSAGE

        elif view == 'delete_user':
            self.build_message(title='🔔 Оповещение',
                               description='Вы были удалены из системы.')
            return self.MESSAGE
