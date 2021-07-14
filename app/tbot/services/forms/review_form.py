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
                self.extend_keyboard(False, BUTTONS_TEMPLATES['review_form_duties_list'],
                                     BUTTONS_TEMPLATES['review_form_projects_list'], )
                self.extend_keyboard(True, BUTTONS_TEMPLATES['review_form_achievements_list'],
                                     BUTTONS_TEMPLATES['review_form_fails'])
                if form.achievements and form.fails and form.projects and form.duties:
                    if form.user.boss:
                        self.extend_keyboard(True, BUTTONS_TEMPLATES['review_form_send_to_boss'])
                    elif form.coworker_reviews:
                        self.extend_keyboard(True, BUTTONS_TEMPLATES['review_send_coworkers'].add(form=form.id))
                return self.build(form=form.id)

            elif review_type == 'boss':
                self.extend_keyboard(False, BUTTONS_TEMPLATES['boss_review_accept'],
                                     BUTTONS_TEMPLATES['boss_review_decline'])
                self.extend_keyboard(True, BUTTONS_TEMPLATES['boss_review_list'])
                markup = self.build(review=review.id)
                return markup

            elif review_type == 'coworker':
                self.extend_keyboard(False, BUTTONS_TEMPLATES['coworker_projects'])
                self.extend_keyboard(True, BUTTONS_TEMPLATES['coworker_review_advices_todo'].add(type='todo'),
                                     BUTTONS_TEMPLATES['coworker_review_advices_not_todo'].add(type='not todo'))
                if review.advices and any(advice.advice_type.name == 'todo' for advice in review.advices) \
                    and any(advice.advice_type.name == 'not todo' for advice in review.advices) \
                    and all(rating.text and rating.rating for rating in review.projects_ratings):
                    self.extend_keyboard(True, BUTTONS_TEMPLATES['coworker_review_form_send_to_hr'])
                self.extend_keyboard(True, BUTTONS_TEMPLATES['coworker_review_list'])
                markup = self.build(review=review.id)
                return markup

            elif review_type == 'hr':

                if self.args.get('accept'):
                    pass

                elif self.args.get('decline'):
                    self.extend_keyboard(False, BUTTONS_TEMPLATES['hr_review_todo'].add(type='todo'),
                                         BUTTONS_TEMPLATES['hr_review_not_todo'].add(type='not todo'),
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
            fill_instance = ''
            if form.duties:
                fill_volume += 1
                list_text = [f'{duty.text}' for duty in form.duties]
                self.build_list_message(title='▪️Обязанности', list_text=list_text)
            else:
                fill_instance += '\n❌  Вы не заполнили раздел “Обязанности”'

            if form.projects:
                fill_volume += 1
                find_coworkers = lambda project: '\n'.join(
                    [f"• {review.coworker.fullname} (@{review.coworker.username})" for review in project.reviews])
                project_list_text = [
                    f'<b>{project.name}</b>\n<i>{project.description}</i>\nОценивающие:\n{find_coworkers(project)}'
                    for project in form.projects]
                self.build_list_message(title='▪️Проекты', list_text=project_list_text)

            else:
                fill_instance += '\n❌  Вы не заполнили раздел “Проекты”'

            if form.achievements:
                fill_volume += 1
                list_text = [f'{achievement.text}' for achievement in form.achievements]
                self.build_list_message(title='▪️Достижения', list_text=list_text)
            else:
                fill_instance += '\n❌  Вы не заполнили раздел “Достижения”'

            if form.fails:
                fill_volume += 1
                list_text = [f'{fail.text}' for fail in form.fails]
                self.build_list_message(title='▪️Провалы', list_text=list_text)
            else:
                fill_instance += '\n❌  Вы не заполнили раздел “Провалы”'

            if fill_volume == max_volume:
                filling = f' - Статус: {form.status.name} ✔'
            else:
                filling = f' - Статус: заполнение ({int(fill_volume / max_volume * 100)}%)'
            if fill_volume == 0:
                bot_text = f'<i>Заполни все 4 раздела анкеты для того, чтобы коллеги могли по достоинству оценить ' \
                           f'твою работу. Подсказка: начни с раздела обязанности.</i>\n\n' \
                           f'{filling}'
            else:
                bot_text = f'{filling}'

            if fill_instance:
                bot_text = f'{bot_text}\n\n' \
                           f'❕  Состояние заполнения:' \
                           f'{fill_instance}'
            self.build_message(title='▫️Информация об анкете',
                               text=bot_text)
            if form.boss_review and form.boss_review.text:
                self.build_message(title='▫ Необходимо исправить', text=f' -  {form.boss_review.text}')
            return self.MESSAGE

        elif review_type == 'boss':
            self.build_message(title='📝 Анкета подчинённого', text=f'Сотрудник: {form.user.fullname}')
            if form.duties:
                list_text = [f'{duty.text}' for duty in form.duties]
                self.build_list_message(title='▪️Обязанности', list_text=list_text)
            if form.projects:
                find_coworkers = lambda project: '\n •  '.join(
                    [f"@{review.coworker.username}" for review in project.reviews])
                list_text = [
                    f'{project.name}\n Описание: {project.description}\n Оценивающие:\n •  {find_coworkers(project)}'
                    for project in
                    form.projects]
                self.build_list_message(title='▪️Проекты', list_text=list_text)
            if form.achievements:
                list_text = [f'{achievement.text}' for achievement in form.achievements]
                self.build_list_message(title='▪️Достижения', list_text=list_text)
            if form.fails:
                list_text = [f'{fail.text}' for fail in form.fails]
                self.build_list_message(title='▪️Провалы', list_text=list_text)

            if review.text:
                self.build_message(title='▫ Ваш крайний комментарий', text=f' -  {review.text}')
            if view == 'decline':
                self.build_message(description='❕ Напишите, что исправить или добавить в анкету.')
            return self.MESSAGE

        elif review_type == 'coworker':
            self.build_message(title='📝 Анкета коллеги',
                               text=f'Сотрудник: @{form.user.username} - {form.user.fullname}\n'
                                    f'Оценивающий: @{review.coworker.username} – {review.coworker.fullname}')
            if form.duties:
                list_text = [f'{duty.text}' for duty in form.duties]
                self.build_list_message(title='▪️Обязанности', list_text=list_text)
            if form.projects:
                find_coworkers = lambda project: '\n •  '.join(
                    [f"@{review.coworker.username}" for review in project.reviews])
                list_text = [
                    f'{project.name}\n Описание: {project.description}\n Оценивающие:\n •  {find_coworkers(project)}'
                    for project in
                    form.projects]
                self.build_list_message(title='▪️Проекты', list_text=list_text)
            if form.achievements:
                list_text = [f'{achievement.text}' for achievement in form.achievements]
                self.build_list_message(title='▪️Достижения', list_text=list_text)
            if form.fails:
                list_text = [f'{fail.text}' for fail in form.fails]
                self.build_list_message(title='▪️Провалы', list_text=list_text)

            list_data = []
            for rating in ratings:
                if rating.text or rating.rating:
                    list_data.append(f'{rating.project.name}')
                if rating.rating:
                    list_data[-1] += f'\n -  Оценка: {rating.rating.name} {"🌟" * rating.rating.value}'
                if rating.text:
                    list_data[-1] += f'\n -  Комментарий: {rating.text}'
                if rating.hr_comment:
                    list_data[-1] += f'<i>\n❗ Исправить: {rating.hr_comment}</i>'
            if list_data:
                self.build_list_message(title='▫ Оценки коллеги', list_text=list_data)

            if review.advices:
                todo = []
                not_todo = []
                for advice in review.advices:
                    if advice.advice_type.name == 'todo':
                        todo.append(advice)
                    else:
                        not_todo.append(advice)
                self.build_message(title='▫ Советы коллеги')
                if todo:
                    for i, advice in enumerate(todo):
                        if i > 0:
                            text = f'{text}\n• {advice.text}'
                        else:
                            text = f'• {advice.text}'
                        if advice.hr_comment:
                            sub_text = f'<i>❗ Исправить: {advice.hr_comment}</i>'
                            text = f'{text}\n{sub_text}'
                    self.build_message(title='Что начать делать:',
                                       text=text)
                if not_todo:
                    for i, advice in enumerate(not_todo):
                        if i > 0:
                            text = f'{text}\n• {advice.text}'
                        else:
                            text = f'• {advice.text}'
                        if advice.hr_comment:
                            sub_text = f'<i>❗ Исправить: {advice.hr_comment}</i>'
                            text = f'{text}\n{sub_text}'
                    self.build_message(title='Что перестать делать:',
                                       text=text)
            if not any(advice.hr_comment for advice in review.advices) and not any(
                rating.hr_comment for rating in ratings):
                count_comment = 0
                count_rate = 0
                max_rates = len(review.projects_ratings) or 1
                for rating in review.projects_ratings:
                    if rating.text:
                        count_comment += 1
                    if rating.rating:
                        count_rate += 1
                ratings_percent = int(count_rate / max_rates * 100)
                rating_mark = '✅' if ratings_percent == 100 else '❌'
                comments_percent = int(count_comment / max_rates * 100)
                comments_mark = '✅' if comments_percent == 100 else '❌'

                self.build_message(description=f'❕ Состояние заполнения\n'
                                               f' {rating_mark}  Вы оценили {int(count_rate / max_rates * 100)}% проектов\n'
                                               f' {comments_mark}  Вы прокомментировали {int(count_comment / max_rates * 100)}% проектов\n'
                                               f' {"✅" if review.advices and any(advice.advice_type.name == "todo" for advice in review.advices) else "❌"}  "Что делать?"\n'
                                               f' {"✅" if review.advices and any(advice.advice_type.name == "not todo" for advice in review.advices) else "❌"}  "Что перестать делать?"\n')
            return self.MESSAGE

        elif review_type == 'hr':
            self.build_message(title='📝 Анкета коллеги',
                               text=f'Сотрудник: @{form.user.username} - {form.user.fullname}')
            if form.duties:
                list_text = [f'{duty.text}' for duty in form.duties]
                self.build_list_message(title='▪️Обязанности', list_text=list_text)
            if form.projects:
                find_coworkers = lambda project: '\n •  '.join(
                    [f"@{review.coworker.username}" for review in project.reviews])
                list_text = [
                    f'{project.name}\n Описание: {project.description}\n Оценивающие:\n •  {find_coworkers(project)}'
                    for project in
                    form.projects]
                self.build_list_message(title='▪️Проекты', list_text=list_text)
            if form.achievements:
                list_text = [f'{achievement.text}' for achievement in form.achievements]
                self.build_list_message(title='▪️Достижения', list_text=list_text)
            if form.fails:
                list_text = [f'{fail.text}' for fail in form.fails]
                self.build_list_message(title='▪️Провалы', list_text=list_text)

            list_data = []
            for rating in ratings:
                if rating.text or rating.rating:
                    list_data.append(f'{rating.project.name}')
                if rating.rating:
                    list_data[-1] += f'\nОценка: {rating.rating.name} {"🌟" * rating.rating.value}'
                if rating.text:
                    list_data[-1] += f'\nКомментарий: {rating.text}'
                if rating.hr_comment:
                    list_data[-1] += f'<i>\n❗ Исправить: {rating.hr_comment}</i>'
            if list_data:
                self.build_list_message(title='▫ Ваши оценки', list_text=list_data)

            if review.advices:
                todo = []
                not_todo = []
                for advice in review.advices:
                    if advice.advice_type.name == 'todo':
                        todo.append(advice)

                    else:
                        not_todo.append(advice)

                self.build_message(title='▫ Ваши советы')
                if todo:
                    for i, advice in enumerate(todo):
                        if i > 0:
                            text = f'{text}\n• {advice.text}'
                        else:
                            text = f'• {advice.text}'
                        if advice.hr_comment:
                            sub_text = f'<i>❗ Исправить: {advice.hr_comment}</i>"'
                            text = f'{text}\n{sub_text}'
                    self.build_message(title='Что начать делать:',
                                       text=text)
                if not_todo:
                    for i, advice in enumerate(not_todo):
                        if i > 0:
                            text = f'{text}\n• {advice.text}'
                        else:
                            text = f'• {advice.text}'
                        if advice.hr_comment:
                            sub_text = f'<i>❗ Исправить: {advice.hr_comment}</i>"'
                            text = f'{text}\n{sub_text}'
                    self.build_message(title='Что перестать делать:',
                                       text=text)
            if view == 'todo':
                self.build_message(description='❕ Введите, что исправить в разделе "Ваши советы".')
            return self.MESSAGE

        elif review_type == 'not_active':
            self.build_message(description='❕ В данный момент анкетирование не проходит.')
            return self.MESSAGE


__all__ = ['ReviewForm']
