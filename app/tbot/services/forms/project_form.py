from telebot.types import InlineKeyboardMarkup

from app.models import Project
from app.services.dictinary.rating import RatingService
from app.tbot.extensions.template import Template
from app.tbot.storages import BUTTONS_TEMPLATES
from configs.bot_config import MAX_USERS_ON_PROJECT


class ProjectForm(Template):
    """ Шаблон формы проектов """

    def create_markup(self) -> InlineKeyboardMarkup:
        """ Создать клавиатуру """
        if self.args.get('have_markup'):
            review_type = self.args.get('review_type')
            review = self.args.get('review')
            project = self.args.get('project')
            coworker_comment_rating = self.args.get('rating')
            view = self.args.get('view')
            if review_type == 'write':
                if view == 'delete_choose_contact':
                    main_template = BUTTONS_TEMPLATES['review_form_project_delete_contact']
                    self.extend_keyboard(True, BUTTONS_TEMPLATES['review_form_project_contacts_back'])
                    return self.build_list(main_template,
                                           unique_args=[{'contact': review.coworker.id} for review in project.reviews],
                                           project=project.id)
                elif view == 'edit_choose_contact':
                    main_template = BUTTONS_TEMPLATES['review_form_project_edit_contact']
                    self.extend_keyboard(True, BUTTONS_TEMPLATES['review_form_project_contacts_back'])
                    return self.build_list(main_template,
                                           unique_args=[{'contact': review.coworker.id} for review in project.reviews],
                                           project=project.id)
                elif view == 'contacts':
                    if len(project.reviews) < MAX_USERS_ON_PROJECT:
                        self.extend_keyboard(False, BUTTONS_TEMPLATES['review_form_add_contact_in_current_project'])
                    if project.reviews:
                        self.extend_keyboard(True, BUTTONS_TEMPLATES['review_form_project_delete_choose_contact'],
                                             BUTTONS_TEMPLATES['review_form_project_edit_choose_contact'])
                    self.extend_keyboard(True, BUTTONS_TEMPLATES['review_form_project_edit_back'])
                    return self.build(project=project.id)
                else:
                    self.extend_keyboard(False, BUTTONS_TEMPLATES['review_form_project_edit_name'],
                                         BUTTONS_TEMPLATES['review_form_project_edit_description'],
                                         BUTTONS_TEMPLATES['review_form_project_contacts'])
                    self.extend_keyboard(True, BUTTONS_TEMPLATES['review_form_back_projects_list'])
                    return self.build(project=project.id)

            elif review_type == 'coworker':
                if view == 'rate':
                    unique_args = [{'rate': rating.id} for rating in RatingService().all]
                    rate = BUTTONS_TEMPLATES['coworker_rate']
                    back = BUTTONS_TEMPLATES['coworker_back_project']
                    back_to_projects = BUTTONS_TEMPLATES['coworker_back_projects'].add(review=review.id)
                    target = coworker_comment_rating.rating.value if coworker_comment_rating.rating else None
                    self.extend_keyboard(True, back, back_to_projects)
                    return self.build_list(rate, unique_args=unique_args, target=target,
                                           proj_rate=coworker_comment_rating.id,
                                           review=review.id)
                elif view == 'project':
                    self.extend_keyboard(True, BUTTONS_TEMPLATES['coworker_choose_rate'],
                                         BUTTONS_TEMPLATES['coworker_comment'])
                    self.extend_keyboard(True, BUTTONS_TEMPLATES['coworker_back_projects'].add(review=review.id))
                    return self.build(proj_rate=coworker_comment_rating.id, review=review.id)

    def add_project(self, project: Project):
        """ Добавить проект в сообщение """
        list_text = ''
        text_rim = len(project.reviews)
        for i, review in enumerate(project.reviews):
            list_text = f'{list_text}{i + 1}){review.coworker.fullname} (@{review.coworker.username})'
            if i + 1 != text_rim:
                list_text = f'{list_text}\n'

        self.build_message(title='Проект:',
                           text=project.name)
        self.build_message(title='Роль и результаты:',
                           text=project.description)
        self.build_message(title='Оценивающие:',
                           text=list_text)

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """
        review_type = self.args.get('review_type')
        project = self.args.get('project')
        coworker_comment_rating = self.args.get('rating')
        view = self.args.get('view')
        if review_type == 'coworker':
            self.add_project(project)

            if coworker_comment_rating.rating:
                if coworker_comment_rating.rating.value == -1:
                    text = f'✖'
                else:
                    text = f'{"🌟" * coworker_comment_rating.rating.value}'
                self.build_message(title='Текущая оценка:', text=text)
            if coworker_comment_rating.text:
                self.build_message(title='Комментарий к проекту:', text=coworker_comment_rating.text)
            if coworker_comment_rating.hr_comment:
                self.build_message(description=f'Замечания от HR: {coworker_comment_rating.hr_comment}')
            if view == 'comment':
                self.build_message(description='❕ Напишите свой комментарий к проекту.')
            elif view == 'rate':
                text = ''
                for i, rating in enumerate(RatingService().all):
                    if rating.value == -1:
                        text = f'{text}✖ - {rating.name}\n'
                    else:
                        text = f'{text}{"🌟" * rating.value} - {rating.name}\n'
                self.build_message(description='❕ Поставьте оценку проекту',
                                   text=text)
            return self.MESSAGE

        elif review_type == 'hr':
            self.add_project(project)
            if coworker_comment_rating.rating.value == -1:
                text = '✖'
            else:
                text = f'{"🌟" * coworker_comment_rating.rating.value}'
            self.build_message(title='Текущая оценка:', text=text)
            self.build_message(title='Комментарий к проекту:', text=coworker_comment_rating.text)
            if coworker_comment_rating.hr_comment:
                self.build_message(description='❕ Введите, что исправить оценивающему в своей оценке и комментарие.')
            return self.MESSAGE

        elif review_type == 'write':

            if view == 'edit':
                self.add_project(project)
                self.build_message(description='❕ Выберите, что именно вы хотите изменить в проекте:')

            elif view == 'edit_name':
                self.add_project(project)
                self.build_message(description='❕ Напишите название проекта.')

            elif view == 'edit_description':
                self.add_project(project)
                self.build_message(description='❕ Опишите цель проекта и свои обязанности.')

            elif view == 'edit_coworkers':
                self.add_project(project)
                self.build_message(description='❕ Перечисли через “;” username коллег:')

            elif view == 'change_coworker':
                self.add_project(project)
                self.build_message(description='❕ Введите username коллеги:')

            elif view == 'contacts':
                self.add_project(project)
                self.build_message(description='❕ Внеси изменения или вернись к списку проектов.')
                if len(project.reviews) >= MAX_USERS_ON_PROJECT:
                    self.build_message(description=f'Максимальное число оценивающих в проекте - {MAX_USERS_ON_PROJECT}')

            elif view == 'delete_choose_contact':
                self.add_project(project)
                self.build_message(description='❕ Выберите коллегу, которого вы хотите убрать из проекта.')

            elif view == 'edit_choose_contact':
                self.add_project(project)
                self.build_message(description='❕ Выберите коллегу, которого вы хотите поменять на другого.')

            elif not project.name:
                self.build_message(title='Заполнение проекта',
                                   description='❕ Напишите название проекта')

            elif not project.description:
                self.build_message(title='Заполнение проекта',
                                   description='\n❕ Опиши полученные результаты и свою роль в этом проекте:',
                                   text=f'\n<b>Название проекта:</b>\n {project.name}')

            elif not project.reviews:
                self.build_message(title='Заполнение проекта',
                                   description='\n❕ Перечисли через “;” имена коллег с использованием @:',
                                   text=f'\n<b>Название проекта:</b>\n {project.name}\n'
                                        f'<b>Роль и результаты:</b>\n {project.description}\n\n'
                                        f'Введи username коллег, которые могут оценить твой вклад в этот проект: '
                                        f'коллеги по команде, все, с кем пересекались по этой задаче, твой наставник, '
                                        f'твои подчиненные и стажеры.\n\n'
                                        f'Руководителя добавлять не нужно – если ты указал его ник при регистрации, '
                                        f'он автоматически оценит все твои проекты.')
            else:
                coworkers = ' '.join(
                    [f'{review.coworker.fullname} (@{review.coworker.username})' for review in project.reviews])
                self.build_message(title=f'Проект - {project.name}', text=f'Роль и результаты: {project.description}\n'
                                                                          f'Коллеги: {coworkers}')
            return self.MESSAGE


__all__ = ['ProjectForm']
