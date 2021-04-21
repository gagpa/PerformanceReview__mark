from telebot.types import InlineKeyboardMarkup

from app.tbot.extensions.template import Template
from app.tbot.storages import BUTTONS_TEMPLATES


class ReviewForm(Template):
    """ Шаблон формы анкеты """

    def create_markup(self) -> InlineKeyboardMarkup:
        if self.args.get('have_markup'):
            rows = []
            form = self.args.get('form')
            advice = self.args.get('advice')
            review_type = self.args.get('review_type')
            review = self.args.get('review')
            if review_type == 'write':
                self.extend_keyboard(False, BUTTONS_TEMPLATES['review_form_duty'],
                                     BUTTONS_TEMPLATES['review_form_projects_list'], )
                self.extend_keyboard(True, BUTTONS_TEMPLATES['review_form_achievements_list'],
                                     BUTTONS_TEMPLATES['review_form_fails'])
                if form.achievements and form.fails and form.projects and form.duty:
                    self.extend_keyboard(True, BUTTONS_TEMPLATES['review_form_send_to_boss'])
                return self.build(form=form.id)

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
        fill_volume = 0
        max_volume = 4
        if review_type == 'write':
            self.build_message(title='📝 Анкета')

        if form.duty:
            fill_volume += 1
            self.build_message(title='▪️Обязанности', text=f' -  {form.duty.text}')
        if form.achievements:
            fill_volume += 1
            list_text = [f'{achievement.text}' for achievement in form.achievements]
            self.build_list_message(title='▪️Достижения', list_text=list_text)
        if form.fails:
            fill_volume += 1
            list_text = [f'{fail.text}' for fail in form.fails]
            self.build_list_message(title='▪️Провалы', list_text=list_text)
        if form.projects:
            fill_volume += 1
            find_coworkers = lambda project: '\n -  '.join([f"@{review.coworker.username}" for review in project.reviews])
            list_text = [f'{project.name}\n -  {project.description}\n -  {find_coworkers(project)}' for project in
                         form.projects]
            self.build_list_message(title='▪️Проекты', list_text=list_text)

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
                    list_data.append(
                        f'{rating.project.name}\n- Оценка: {f"{rating.rating.name} {rating.text}" if rating.rating else "Не стоит"}')
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
            self.build_message(
                description=f'Оценивающий @{advice.coworker_review.coworker.username}\nВладелец формы @{form.user.username}')
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

        elif review_type == 'write':
            if fill_volume == max_volume:
                filling = f' -  Статус: заполнена ✔'
            else:
                filling = f' -  Статус: заполнение ({int(fill_volume / max_volume * 100)}%)'
            self.build_message(title='▫️Информация об анкете',
                               text=f' -  Опрос закончится: {form.review_period.end_date}\n'
                                    f'{filling}')
            if form.boss_review:
                self.build_message(title='▫ Необходимо исправить', text=f' -  {form.boss_review.text}')

            return self.MESSAGE


__all__ = ['ReviewForm']
