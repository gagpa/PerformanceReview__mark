from telebot.types import InlineKeyboardMarkup

from app.tbot.extensions.template import Template
from app.tbot.storages import BUTTONS_TEMPLATES


class ProjectsForm(Template):
    """ Шаблон формы проектов """

    def create_markup(self) -> InlineKeyboardMarkup:
        """ Создать клавиатуру """
        rows = []
        if self.args.get('have_markup'):
            form = self.args.get('form')
            review_type = self.args.get('review_type')
            review = self.args.get('review')
            projects = self.args.get('projects')
            ratings = self.args.get('ratings')
            page = self.args.get('page')
            view = self.args.get('view')
            if review_type == 'write':
                if view == 'delete_choose':
                    unique_args = [{'project': project.id} for project in projects]
                    main_template = BUTTONS_TEMPLATES['review_form_project_delete']
                    self.extend_keyboard(True, BUTTONS_TEMPLATES['review_form_back_projects_list'])
                    return self.build_list(main_template, unique_args)
                elif view == 'edit_choose':
                    unique_args = [{'project': project.id} for project in projects]
                    main_template = BUTTONS_TEMPLATES['review_form_project_edit']
                    self.extend_keyboard(True, BUTTONS_TEMPLATES['review_form_back_projects_list'])
                    return self.build_list(main_template, unique_args)
                elif view == 'list':
                    self.extend_keyboard(False, BUTTONS_TEMPLATES['review_form_project_add'])
                    if projects:
                        self.extend_keyboard(True, BUTTONS_TEMPLATES['review_form_project_edit_choose'],
                                             BUTTONS_TEMPLATES['review_form_project_delete_choose'])
                    self.extend_keyboard(True, BUTTONS_TEMPLATES['review_form'])
                    return self.build()

            elif review_type == 'coworker':
                ratings = self.cut_per_page(ratings, page)
                unique_args = [{'proj_rate': rating.id} for rating in ratings]
                main_template = BUTTONS_TEMPLATES['coworker_project']
                pagination_template = BUTTONS_TEMPLATES['coworker_projects'].add(review=review.id)
                back = BUTTONS_TEMPLATES['coworker_back_form'].add(review=review.id)
                self.extend_keyboard(False, back)
                self.add_paginator(paginator=pagination_template, page=page, count_obj=len(ratings))
                return self.build_list(main_template, unique_args)

            elif review_type == 'hr':
                ratings = self.cut_per_page(ratings, page)
                main_template = BUTTONS_TEMPLATES['hr_review_comment_rating']
                back = BUTTONS_TEMPLATES['hr_review_back_to_decline'].add(review=review.id)
                pagination_template = BUTTONS_TEMPLATES['hr_review_ratings'].add(review=review.id)
                unique_args = [{'proj_rate': rating.id} for rating in ratings]
                self.extend_keyboard(False, back)
                self.add_paginator(paginator=pagination_template, page=page, count_obj=len(ratings))
                return self.build_list(main_template, unique_args)

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """
        review_type = self.args.get('review_type')
        review = self.args.get('review')
        projects = self.args.get('projects')
        page = self.args.get('page')
        ratings = self.args.get('ratings')
        form = self.args.get('form')
        view = self.args.get('view')
        title = 'Проекты'
        if review_type == 'hr':
            list_data = [f'{project.name}\n{project.description}' for project in projects]
            self.build_list_message(title='Проверка оценок проектов',
                                    description=f'Автор: @{form.user.username}\n'
                                                f'Проверяющий: @{review.coworker.username}',
                                    list_text=list_data)
            if ratings:
                list_data = []
                for rating in ratings:
                    list_data.append(
                        f'{rating.project.name}\n- Оценка: {f"{rating.rating.name} {rating.text}" if rating.rating else "Не стоит"}')
                    if rating.hr_comment:
                        list_data[-1] += f'\n- Крайний комментарий HR: {rating.hr_comment}'
                self.build_list_message(title='Оценки', description='', list_text=list_data)
            return self.MESSAGE

        elif review_type == 'coworker':
            list_data = [f'{project.name}\n{project.description}' for project in projects]
            self.build_list_message(title='Проекты на оценку', description=f'Коллега: {form.user.fullname}',
                                    list_text=list_data)
            if ratings:
                list_data = []
                for rating in ratings:
                    list_data.append(
                        f'{rating.project.name}\n- Оценка: {f"{rating.rating.name} {rating.text}" if rating.rating else "Не стоит"}')
                    if rating.hr_comment:
                        list_data[-1] += f'\n- Исправить: {rating.hr_comment}'
                self.build_list_message(title='Ваши оценки', description='', list_text=list_data)
            return self.MESSAGE

        elif review_type == 'write':
            title = '▪️Проекты'
            find_coworkers = lambda project: '\n -  '.join(
                [f"@{review.coworker.username}" for review in project.reviews])
            if view == 'list':
                if projects:
                    list_text = [f'{project.name}\n -  {project.description}\n -  {find_coworkers(project)}' for project in projects]
                    self.build_list_message(title=title,
                                            description='\nДобавьте проекты, которые ты выполнял, или измените их',
                                            list_text=list_text)
                else:
                    self.build_message(title=title, description='Добавьте проекты, которые ты выполнял')
                return self.MESSAGE

            elif view == 'edit_choose':
                list_text = [f'{project.name}\n -  {project.description}\n -  {find_coworkers(project)}' for project in projects]
                self.build_list_message(title=title,
                                        description='\nВыберите проект, который хотите изменить',
                                        list_text=list_text)

            elif view == 'delete_choose':
                list_text = [f'{project.name}\n -  {project.description}\n -  {find_coworkers(project)}' for project in projects]
                self.build_list_message(title=title,
                                        description='\nВыберите проект, который хотите удалить',
                                        list_text=list_text)
            return self.MESSAGE


__all__ = ['ProjectsForm']
