from telebot.types import InlineKeyboardMarkup

from app.tbot.extensions.template import Template
from app.tbot.storages import BUTTONS_TEMPLATES


class CoworkerAdvicesForm(Template):
    """ Шаблон формы советов """

    def create_markup(self) -> InlineKeyboardMarkup:
        """ Создать клавиатуру """
        view = self.args.get('view')
        coworker_advices = self.args.get('coworker_advices')
        review = self.args.get('review')
        advice_type = self.args.get('advice_type')
        if view == 'list':
            self.extend_keyboard(False, BUTTONS_TEMPLATES['coworker_review_advices_add'])
            if coworker_advices:
                self.extend_keyboard(True, BUTTONS_TEMPLATES['coworker_review_advices_edit_choose'],
                                     BUTTONS_TEMPLATES['coworker_review_advices_delete_choose'])
            self.extend_keyboard(True, BUTTONS_TEMPLATES['coworker_back_form'])
            return self.build(review=review.id, type=advice_type)

        elif view == 'delete_choose':
            unique_args = [{'coworker_advice': coworker_advice.id} for coworker_advice in coworker_advices]
            main = BUTTONS_TEMPLATES['coworker_review_advices_delete']
            self.extend_keyboard(True, BUTTONS_TEMPLATES['coworker_review_back_advices'],
                                 BUTTONS_TEMPLATES['coworker_back_form'])
            return self.build_list(main, unique_args, review=review.id, type=advice_type)

        elif view == 'edit_choose':
            unique_args = [{'coworker_advice': coworker_advice.id} for coworker_advice in coworker_advices]
            main = BUTTONS_TEMPLATES['coworker_review_advices_edit']
            self.extend_keyboard(True, BUTTONS_TEMPLATES['coworker_review_back_advices'],
                                 BUTTONS_TEMPLATES['coworker_back_form'])
            return self.build_list(main, unique_args, review=review.id, type=advice_type)
        elif view == 'hr':
            unique_args = [{'coworker_advice': coworker_advice.id} for coworker_advice in coworker_advices]
            main = BUTTONS_TEMPLATES['hr_advices_edit']
            self.extend_keyboard(True, BUTTONS_TEMPLATES['hr_review_back_to_decline'],
                                 BUTTONS_TEMPLATES['hr_review_back_to_form_name'])
            return self.build_list(main, unique_args, review=review.id, type=advice_type)

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """
        view = self.args.get('view')
        coworker_advices = self.args.get('coworker_advices')
        advice_type = self.args.get('advice_type')
        if advice_type == 'todo':
            title = '▪️Что делать?'
        elif advice_type == 'not todo':
            title = '▪️Что перестать делать?'
        else:
            title = '▪️Советы'
        list_text = []
        for advice in coworker_advices:
            text = advice.text
            if advice.hr_comment:
                text = f'{advice.text}\n❗ Исправить: {advice.hr_comment}'
            list_text.append(text)
        if view == 'list':

            if coworker_advices:
                self.build_message(title=title,
                                   description='Ваши советы коллеге')
                if advice_type == 'todo':
                    description = '\n❕ Нажми кнопку “Добавить” и перечисли свои советы и пожелания – через «;». Если что-то забудешь, позже можно это исправить.'
                elif advice_type == 'not todo':
                    description = '\n❕ Нажми кнопку “Добавить” и перечисли что стоит перестать делать коллеге – через «;». Если что-то забудешь, позже можно это исправить.'
                else:
                    description = '\n❕ Нажми кнопку “Добавить” и перечисли свои советы – через «;». Если что-то забудешь, позже можно это исправить.'
                self.build_list_message(description=description,
                                        list_text=list_text)
            return self.MESSAGE

        elif view == 'delete_choose':

            self.build_list_message(title=title,
                                    description='\n❕ Выберите совет, который вы хотите удалить.',
                                    list_text=list_text)
            return self.MESSAGE

        elif view == 'edit_choose':
            self.build_list_message(title=title,
                                    description='\n❕ Выберите совет, который вы хотите изменить.',
                                    list_text=list_text)
            return self.MESSAGE

        elif view == 'add':
            if advice_type == 'todo':
                description = '\n❕ Напиши, что стоит начать делать твоему коллеге, чтобы улучшить свою работу, одним текстом через «;». Если что-то забудешь, позже можно это исправить:'
            else:
                description = '\n❕ Напиши, что стоит перестать делать твоему коллеге, чтобы улучшить свою работу, одним текстом через «;». Если что-то забудешь, позже можно это исправить:'
            if coworker_advices:
                self.build_list_message(title=title,
                                        description=f'\n{description}',
                                        list_text=list_text)
            else:
                self.build_message(title=title, description=description)
            return self.MESSAGE

        elif view == 'hr':
            todo = []
            not_todo = []
            description = '\n❕ Выберите совет, который нужно исправить, или у которого вы хотите убрать свой комментарий'
            for i, advice in enumerate(coworker_advices):

                if advice.hr_comment:
                    text = f'{advice.text}\n❗ Исправить: {advice.hr_comment}'
                else:
                    text = advice.text
                if advice.advice_type.name == 'todo':
                    if not todo:
                        self.build_message(title='Что делать?')
                    todo.append(text)
                else:
                    if not not_todo:
                        self.build_message(title='Что перестать делать?')
                    not_todo.append(text)
            if todo:
                self.build_list_message(list_text=todo, description=description)
            else:
                self.build_list_message(list_text=not_todo, description=description)
            return self.MESSAGE


__all__ = ['CoworkerAdvicesForm']
