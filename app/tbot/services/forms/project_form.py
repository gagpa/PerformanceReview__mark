from telebot.types import InlineKeyboardMarkup

from app.services.dictinary.rating import RatingService
from app.tbot.extensions.template import Template
from app.tbot.storages import BUTTONS_TEMPLATES


class ProjectForm(Template):
    """ Шаблон формы проектов """

    def create_markup(self) -> InlineKeyboardMarkup:
        """ Создать клавиатуру """
        if self.args.get('have_markup'):
            review_type = self.args.get('review_type')
            review = self.args.get('review')
            project = self.args.get('project')
            coworker_comment_rating = self.args.get('rating')

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
        review_type = self.args.get('review_type')
        project = self.args.get('project')
        coworker_comment_rating = self.args.get('rating')
        view = self.args.get('view')
        if review_type == 'coworker':
            description = ''
            for i, rating in enumerate(RatingService().all):
                description += f'\n{"🌟" * rating.value} - {rating.name}'
            text = f' -  Цели и обязаннсоти: {project.description}'
            if coworker_comment_rating.rating:
                text += f'\n -  Текущая оценка: {"🌟" * coworker_comment_rating.rating.value}'
            if coworker_comment_rating.text:
                text += f'\n -  Комментарий к проекту: {coworker_comment_rating.text}'
            self.build_message(title=f'Проект: {project.name}', description=description, text=text)
            if coworker_comment_rating.hr_comment:
                self.build_message(description=f'❗ Исправить: {coworker_comment_rating.hr_comment}')
            if view == 'comment':
                self.build_message(description='❕  Напишите свой комментарий к проекту')
            else:
                self.build_message(description='❕  Поставьте оценку проекту и не забудьте оставить комментарий')
            return self.MESSAGE

        elif review_type == 'hr':
            self.build_message(title=f'Проект: {project.name}',
                               text=f' -  Цели и обязаннсоти: {project.description}\n'
                                    f' -  Текущая оценка: {"🌟" * coworker_comment_rating.rating.value}\n'
                                    f' -  Комментарий к проекту: {coworker_comment_rating.text}')
            if coworker_comment_rating.hr_comment:
                self.build_message(description='❕  Введите, что исправить оценивающему в своей оценке и комментарие')
            return self.MESSAGE

        elif review_type == 'write':
            if view == 'edit':
                coworkers = ' '.join(
                    [f"{review.coworker.fullname} (@{review.coworker.username})" for review in project.reviews])
                self.build_message(title=f'Проект - {project.name}',
                                   description='\n❕  Выберите, что вы хотите изменить в своём проекте',
                                   text=f'Цели и обязаннсоти: {project.description}\n'
                                        f'Коллеги: {coworkers}')

            elif view == 'edit_name':
                coworkers = ' '.join(
                    [f"{review.coworker.fullname} (@{review.coworker.username})" for review in project.reviews])
                self.build_message(title=f'Проект - {project.name}',
                                   description='\n❕  Напишите название проекта',
                                   text=f'Цели и обязаннсоти: {project.description}\n'
                                        f'Коллеги: {coworkers}')

            elif view == 'edit_description':
                coworkers = ' '.join(
                    [f"{review.coworker.fullname} (@{review.coworker.username})" for review in project.reviews])
                self.build_message(title=f'Проект - {project.name}',
                                   description='\n❕  Опишите цель проекта и свои обязанности',
                                   text=f'Цели и обязаннсоти: {project.description}\n'
                                        f'Коллеги: {coworkers}')

            elif view == 'edit_coworkers':
                coworkers = ' '.join(
                    [f"{review.coworker.fullname} (@{review.coworker.username})" for review in project.reviews])
                self.build_message(title=f'Проект - {project.name}',
                                   description='\n❕  Введите username коллеги, который может оценить ваш вклад в проект',
                                   text=f'Цели и обязаннсоти: {project.description}\n'
                                        f'Коллеги: {coworkers}')

            elif not project.name:
                self.build_message(title='Заполнение проекта', description='❕  Напишите название проекта')

            elif not project.description:
                self.build_message(title='Заполнение проекта',
                                   description='\n❕  Опишите цель проекта и свои обязанности',
                                   text=f'Название проекта: {project.name}')

            elif not project.reviews:
                self.build_message(title='Заполнение проекта',
                                   description='\n❕  Введите username коллеги, который может оценить ваш вклад в проект',
                                   text=f'Название проекта: {project.name}\n'
                                        f'Цели и обязаннсоти: {project.description}')
            else:
                coworkers = ' '.join(
                    [f"{review.coworker.fullname} (@{review.coworker.username})" for review in project.reviews])
                self.build_message(title=f'Проект - {project.name}', text=f'Цели и обязаннсоти: {project.description}\n'
                                                                          f'Коллеги: {coworkers}')
            return self.MESSAGE


__all__ = ['ProjectForm']
