from telebot.types import InlineKeyboardMarkup

from app.tbot.extensions.template import Template
from app.tbot.storages import BUTTONS_TEMPLATES


class ProjectsForm(Template):
    """ Шаблон формы проектов """

    def create_markup(self) -> InlineKeyboardMarkup:
        """ Создать клавиатуру """
        if self.args.get('have_markup'):
            form = self.args.get('form')
            review_type = self.args.get('review_type')
            review = self.args.get('review')
            projects = self.args.get('projects')
            ratings = self.args.get('ratings')
            page = self.args.get('page')
            view = self.args.get('view')
            example = self.args.get('example')
            if review_type == 'write':
                if view == 'delete_choose':
                    unique_args = [{'project': project.id} for project in projects]
                    main_template = BUTTONS_TEMPLATES['review_form_project_delete']
                    self.extend_keyboard(True, BUTTONS_TEMPLATES['review_form_back_projects_list'],
                                         BUTTONS_TEMPLATES['review_form'])
                    return self.build_list(main_template, unique_args, prefix='Проект')
                elif view == 'edit_choose':
                    unique_args = [{'project': project.id} for project in projects]
                    main_template = BUTTONS_TEMPLATES['review_form_project_edit']
                    self.extend_keyboard(True, BUTTONS_TEMPLATES['review_form_back_projects_list'],
                                         BUTTONS_TEMPLATES['review_form'])
                    return self.build_list(main_template, unique_args, prefix='Проект')
                elif view == 'list':
                    self.extend_keyboard(False, BUTTONS_TEMPLATES['review_form_project_add'])
                    if projects:
                        self.extend_keyboard(True, BUTTONS_TEMPLATES['review_form_project_edit_choose'],
                                             BUTTONS_TEMPLATES['review_form_project_delete_choose'])
                    elif example:
                        self.extend_keyboard(False, BUTTONS_TEMPLATES['review_form_projects_descriptions'])
                    else:
                        self.extend_keyboard(False, BUTTONS_TEMPLATES['review_form_projects_examples'])
                    self.extend_keyboard(True, BUTTONS_TEMPLATES['review_form'])
                    return self.build()

            elif review_type == 'coworker':
                count_obj = len(ratings)
                ratings = self.cut_per_page(ratings, page)
                unique_args = [{'proj_rate': rating.id} for rating in ratings]
                main_template = BUTTONS_TEMPLATES['coworker_project']
                pagination_template = BUTTONS_TEMPLATES['coworker_projects'].add(review=review.id)
                back = BUTTONS_TEMPLATES['coworker_back_form'].add(review=review.id)
                self.extend_keyboard(False, back)
                self.add_paginator(paginator=pagination_template, page=page, count_obj=count_obj)
                return self.build_list(main_template, unique_args, prefix='Проект')

            elif review_type == 'hr':
                count_obj = len(ratings)
                ratings = self.cut_per_page(ratings, page)
                main_template = BUTTONS_TEMPLATES['hr_review_comment_rating']
                back = BUTTONS_TEMPLATES['hr_review_back_to_decline'].add(review=review.id)
                pagination_template = BUTTONS_TEMPLATES['hr_review_ratings'].add(review=review.id)
                unique_args = [{'proj_rate': rating.id} for rating in ratings]
                self.extend_keyboard(False, back)
                self.add_paginator(paginator=pagination_template, page=page, count_obj=count_obj)
                return self.build_list(main_template, unique_args, prefix='Проект')

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """
        review_type = self.args.get('review_type')
        review = self.args.get('review')
        projects = self.args.get('projects')
        page = self.args.get('page')
        ratings = self.args.get('ratings')
        form = self.args.get('form')
        view = self.args.get('view')
        example = self.args.get('example')
        if page:
            ratings = self.cut_per_page(ratings, page)
            projects = self.cut_per_page(projects, page)
        find_coworkers = lambda project: '\n •  '.join(
            [f"@{review.coworker.username}" for review in project.reviews])
        project_list_text = [
            f'{project.name}\n Роль и результаты: {project.description}\n Оценивающие:\n •  {find_coworkers(project)}'
            for project in
            projects]
        if review_type == 'hr':
            self.build_list_message(title='▪️Проверка оценок проектов',
                                    list_text=project_list_text)
            list_data = []
            for rating in ratings:
                if rating.text or rating.rating:
                    list_data.append(f'{rating.project.name}')
                if rating.rating:
                    list_data[-1] += f'\n -  Оценка: {rating.rating.name} {"🌟" * rating.rating.value}'
                if rating.text:
                    list_data[-1] += f'\n -  Комментарий: {rating.text}'
                if rating.hr_comment:
                    list_data[-1] += f'\n❗ Исправить: {rating.hr_comment}'
            if list_data:
                self.build_list_message(title='▫ Ваши оценки', list_text=list_data)
            self.build_message(description=f'Автор: @{form.user.username}\n'
                                           f'Оценивающий: @{review.coworker.username}')
            self.build_message(description='❕ Выберите проект, у которго необходимо исправить оценку или комментарий.')
            return self.MESSAGE

        elif review_type == 'coworker':

            self.build_list_message(title='▪️Проекты на оценку',
                                    list_text=project_list_text)
            list_data = []
            for rating in ratings:
                if rating.text or rating.rating:
                    list_data.append(f'{rating.project.name}')
                if rating.rating:
                    list_data[-1] += f'\n -  Оценка: {rating.rating.name} {"🌟" * rating.rating.value}'
                if rating.text:
                    list_data[-1] += f'\n -  Комментарий: {rating.text}'
                if rating.hr_comment:
                    list_data[-1] += f'\n❗ Исправить: {rating.hr_comment}'
            if list_data:
                self.build_list_message(title='▫ Ваши оценки', list_text=list_data)
            self.build_message(description='❕ Выберите проект, который вы хотите оценить и прокомментировать.')
            return self.MESSAGE

        elif review_type == 'write':
            title = '▪️Проекты\n'

            if view == 'list':
                if projects:
                    self.build_list_message(title=title,
                                            list_text=project_list_text)
                elif example:
                    self.build_message(title=title,
                                       text='“Проект: Оценка персонала за 1 полугодие 2021\n'
                                            'Описание: Зарегистрировала сотрудников ИЦ в количестве 70 человек\n'
                                            '\nПроект: Коммуникация\n'
                                            'Описание: Опубликовала 15 новостей о работе отделов ИЦ\n'
                                            '\nПроект: Обучение\n'
                                            'Описание: Сходила на тренинг для ботов”\n',
                                       description='❕ Нажми кнопку “Добавить проект” и опиши каждый проект отдельно:')

                else:
                    self.build_message(title=title,
                                       text='Добавь проекты, которые ты делал(-а) последние полгода. Это могут быть:\n'
                                            '– цели твоей команды, на которые ты фактически повлиял(-а),\n'
                                            '– проекты, над которыми ты работал(-а), \n'
                                            '– детали выполнения твоих базовых функциональных обязанностей,\n'
                                            '– планы по росту и развитию.\n',
                                       description='❕ Нажми кнопку “Добавить проект” и опиши каждый проект отдельно:')
                return self.MESSAGE

            elif view == 'edit_choose':
                self.build_list_message(title=title,
                                        description='❕ Выберите проект, который хотите изменить.',
                                        list_text=project_list_text)

            elif view == 'delete_choose':
                self.build_list_message(title=title,
                                        description='❕ Выберите проект, который хотите удалить.',
                                        list_text=project_list_text)
            return self.MESSAGE


__all__ = ['ProjectsForm']
