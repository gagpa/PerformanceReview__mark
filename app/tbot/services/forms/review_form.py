from telebot.types import InlineKeyboardMarkup

from app.tbot.extensions.template import Template
from app.tbot.services.forms.achievements_form import AchievementsForm
from app.tbot.services.forms.duty_form import DutyForm
from app.tbot.services.forms.fails_form import FailsForm
from app.tbot.services.forms.projects_form import ProjectsForm
from app.tbot.storages import BUTTONS_TEMPLATES


class ReviewForm(Template):
    """ Шаблон формы анкеты """
    __ORDER = ['review_form_duty', 'review_form_projects_list', 'review_form_achievements_list', 'review_form_fails']
    templates = {
        'review_form_achievements_list': AchievementsForm(form=True),
        'review_form_duty': DutyForm(form=True),
        'review_form_fails': FailsForm(form=True),
        'review_form_projects_list': ProjectsForm(review_type='write'),
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add()

    def add(self):
        """ Добавить данные из словаря в форму """
        form = self.args['form']
        self.templates['review_form_achievements_list'].args['models'] = form.achievements
        self.templates['review_form_duty'].args['model'] = form.duty
        self.templates['review_form_fails'].args['models'] = form.fails
        self.templates['review_form_projects_list'].args['models'] = form.projects

    def create_markup(self) -> InlineKeyboardMarkup:
        if self.args.get('have_markup'):
            rows = []
            form = self.args.get('form')
            advice = self.args.get('advice')
            review_type = self.args.get('review_type')
            review = self.args.get('review')
            if review_type == 'write':
                rows.append([BUTTONS_TEMPLATES[self.__ORDER[0]], BUTTONS_TEMPLATES[self.__ORDER[1]]])
                rows.append([BUTTONS_TEMPLATES[self.__ORDER[2]], BUTTONS_TEMPLATES[self.__ORDER[3]]])
                rows.append([BUTTONS_TEMPLATES['review_form_send_to_boss']])
                markup = self.markup_builder.build(*rows)
                return markup

            elif review_type == 'boss':
                self.extend_keyboard(False, BUTTONS_TEMPLATES['boss_review_accept'],
                                     BUTTONS_TEMPLATES['boss_review_decline'])
                self.extend_keyboard(True, BUTTONS_TEMPLATES['boss_review_list'])
                markup = self.build(review=review.id)
                return markup

            elif review_type == 'coworker':
                self.extend_keyboard(False, BUTTONS_TEMPLATES['coworker_projects'],
                                     BUTTONS_TEMPLATES['coworker_review_todo'],
                                     BUTTONS_TEMPLATES['coworker_review_not_todo'])
                self.extend_keyboard(True, BUTTONS_TEMPLATES['coworker_review_form_send_to_hr'])
                self.extend_keyboard(False, BUTTONS_TEMPLATES['coworker_review_list'])
                markup = self.build(review=review.id)
                return markup

            elif review_type == 'hr':

                if self.args.get('accept'):
                    pass

                elif self.args.get('decline'):
                    self.extend_keyboard(False, BUTTONS_TEMPLATES['hr_review_todo'],
                                         BUTTONS_TEMPLATES['hr_review_ratings'])
                    self.extend_keyboard(True, BUTTONS_TEMPLATES['hr_review_send_back'])
                    self.extend_keyboard(True, BUTTONS_TEMPLATES['hr_review_back_to_form'])
                    return self.build(review=review.id)

                else:
                    self.extend_keyboard(False, BUTTONS_TEMPLATES['hr_review_accept'],
                                         BUTTONS_TEMPLATES['hr_review_decline'])
                    self.extend_keyboard(True, BUTTONS_TEMPLATES['hr_review_list'])
                    return self.build(review=review.id)

    def create_message(self) -> str:
        form_text = ''
        form = self.args.get('form')
        advice = self.args.get('advice')
        review_type = self.args.get('review_type')
        review = self.args.get('review')
        ratings = self.args.get('ratings')
        view = self.args.get('view')
        for name_template in self.__ORDER:
            form_text += f'{self.templates[name_template].dump()[0]}\n'

        if review_type == 'boss':
            self.build_message(title='Анкета', text=form_text)
            self.build_message(title='', text=f'Сотрудник: {form.user.fullname}')
            if review.text:
                self.build_message(title='Ваш крайний комментарий', text=review.text)
            return self.MESSAGE

        elif review_type == 'coworker':
            self.build_message(title='Анкета', description='', text=form_text)
            self.build_message(title='', description='', text=f'Коллега: {form.user.fullname}')
            if ratings:
                list_data = []
                for rating in ratings:
                    list_data.append(f'{rating.project.name}\n- Оценка: {f"{rating.rating.name} {rating.text}" if rating.rating else "Не стоит"}')
                    if rating.hr_comment:
                        list_data[-1] += f'\n- Исправить: {rating.hr_comment}'
                self.build_list_message(title='Ваши оценки', description='', list_text=list_data)

            if advice:
                self.build_message(title='Что делать/Что не делать?', description='', text='')
                if advice.todo:
                    self.build_message(title='', description='', text=f'- Что делать: {advice.todo}')
                if advice.not_todo:
                    self.build_message(title='', description='', text=f'- Что перестать делать:{advice.not_todo}')
                if advice.hr_comment:
                    self.build_message(title='', description='', text=f'- Исправьте: {advice.hr_comment}')
            if view == 'todo':
                self.build_message(title='', description='Введите "Что стоит изменить вашему коллеги"', text='')
            elif view == 'not todo':
                self.build_message(title='', description='Введите "Что стоит перестать делать вашему коллеги"', text='')

            return self.MESSAGE

        elif review_type == 'hr':
            self.build_message(description=f'Оценивающий @{advice.coworker_review.coworker.username}\nВладелец формы @{form.user.username}')
            self.build_message(title='Анкета', description='', text=form_text)
            if ratings:
                list_data = []
                for rating in ratings:
                    list_data.append(
                        f'{rating.project.name}\n- Оценка: {f"{rating.rating.name} {rating.text}" if rating.rating else "Не стоит"}')
                    if rating.hr_comment:
                        list_data[-1] += f'\n- Комментарий HR: {rating.hr_comment}'
                self.build_list_message(title='Ваши оценки', description='', list_text=list_data)

            if advice:
                self.build_message(title='Что делать/Что не делать?', description='', text='')
                if advice.todo:
                    self.build_message(title='', description='', text=f'- Что делать: {advice.todo}')
                if advice.not_todo:
                    self.build_message(title='', description='', text=f'- Что перестать делать:{advice.not_todo}')
                if advice.hr_comment:
                    self.build_message(title='', description='', text=f'- Комментарий HR: {advice.hr_comment}')

            return self.MESSAGE

        else:
            title = '[АНКЕТА]'
            description = f'Review период:{form.review_period}\n' \
                          f'Статус формы: {form.status.name}'

            message_text = self.message_builder.build_message(title=title,
                                                              description=description,
                                                              text=form_text)
            return message_text


__all__ = ['ReviewForm']
