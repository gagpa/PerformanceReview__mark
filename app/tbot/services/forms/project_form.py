from telebot.types import InlineKeyboardMarkup

from app.services.dictinary.rating import RatingService
from app.tbot.extensions import InlineKeyboardBuilder
from app.tbot.extensions.template import Template
from app.tbot.storages import BUTTONS_TEMPLATES


class ProjectForm(Template):
    """ Шаблон формы проектов """

    def create_markup(self) -> InlineKeyboardMarkup:
        """ Создать клавиатуру """
        if self.args.get('have_markup'):
            form = self.args.get('form')
            review_type = self.args.get('review_type')
            review = self.args.get('review')
            project = self.args.get('project')
            coworker_comment_rating = self.args.get('rating')
            page = self.args.get('page')

            if review_type == 'write':
                self.extend_keyboard(False, BUTTONS_TEMPLATES['review_form_project_edit_name'],
                                     BUTTONS_TEMPLATES['review_form_project_edit_description'],
                                     BUTTONS_TEMPLATES['review_form_project_edit_contacts'])
                self.extend_keyboard(True, BUTTONS_TEMPLATES['review_form_back_projects_list'])
                return self.build(project=project.id)

            elif review_type == 'coworker':
                unique_args = [{'rate': rating.id} for rating in RatingService().all]
                rate = BUTTONS_TEMPLATES['coworker_rate']
                comment = BUTTONS_TEMPLATES['coworker_comment']
                back = BUTTONS_TEMPLATES['coworker_back_projects'].add(review=review.id)
                self.extend_keyboard(False, comment)
                self.extend_keyboard(True, back)
                return self.build_list(rate, unique_args=unique_args, proj_rate=coworker_comment_rating.id,
                                       review=review.id)

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """
        title = 'Проект'
        text = ''
        form = self.args.get('form')
        review_type = self.args.get('review_type')
        review = self.args.get('review')
        project = self.args.get('project')
        coworker_comment_rating = self.args.get('rating')
        page = self.args.get('page')
        view = self.args.get('view')
        if review_type == 'coworker':
            self.build_message(title=project.name, text=f'{project.description}')
            description = 'Оцените проект от 1 🌟 до 5 🌟\n'
            for i, rating in enumerate(RatingService().all):
                description += f'{"🌟" * rating.value} - {rating.name}\n'
            self.build_message(description=description)
            if coworker_comment_rating.rating:
                self.build_message(title='Текущая оценка', text='🌟' * coworker_comment_rating.rating.value)
            if coworker_comment_rating.text:
                self.build_message(title='Комментарий', text=coworker_comment_rating.text)
            if view == 'comment':
                self.build_message(description='❕  Напишите свой комментарий к проекту')
            return self.MESSAGE

        elif review_type == 'hr':
            self.build_message(title='Комментарий для оценивающего',
                               text=f'Название - {self.args["project"].name}\n' \
                                    f'Описание - {self.args["project"].description}\n')
            if coworker_comment_rating.rating:
                self.build_message(title='Текущая оценка', text='🌟' * coworker_comment_rating.rating.value)
            if coworker_comment_rating.text:
                self.build_message(title='Комментарий к проекту', text=coworker_comment_rating.text)
            if coworker_comment_rating.hr_comment:
                self.build_message(title='Комментарий HR', text=coworker_comment_rating.hr_comment)
            return self.MESSAGE

        elif review_type == 'write':
            if not project.name:
                self.build_message(title='Заполнение проекта', description='Напишите название проекта')
            elif not project.description:
                self.build_message(title='Заполнение проекта', description='\nОпишите цель проекта и свои обязанности',
                                   text=f'Название проекта: {project.name}')
            elif not project.reviews:
                self.build_message(title='Заполнение проекта',
                                   description='\nВведите username коллеги, который может оценить ваш вклад в проект',
                                   text=f'Название проекта: {project.name}\n'
                                        f'Цели и обязаннсоти: {project.description}')
            else:
                coworkers = ' '.join([f"@{review.coworker.username}" for review in project.reviews])
                self.build_message(title=f'Проект - {project.name}', text=f'Цели и обязаннсоти: {project.description}\n'
                                                                          f'Коллеги: {coworkers}')
            return self.MESSAGE


__all__ = ['ProjectForm']
