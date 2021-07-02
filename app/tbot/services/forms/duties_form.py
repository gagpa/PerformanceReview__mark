from telebot.types import InlineKeyboardMarkup

from app.tbot.extensions.template import Template
from app.tbot.storages import BUTTONS_TEMPLATES


class DutiesForm(Template):
    """ Шаблон формы обязанностей """

    def create_markup(self) -> InlineKeyboardMarkup:
        """ Создать клавиатуру """
        view = self.args.get('view')
        duties = self.args.get('duties')
        if view == 'list':
            self.extend_keyboard(False, BUTTONS_TEMPLATES['review_form_duties_add'])
            if duties:
                self.extend_keyboard(True, BUTTONS_TEMPLATES['review_form_duties_edit_choose'],
                                     BUTTONS_TEMPLATES['review_form_duties_delete_choose'])
            self.extend_keyboard(True, BUTTONS_TEMPLATES['review_form'])
            return self.build()

        elif view == 'delete_choose':
            unique_args = [{'duty': duty.id} for duty in duties]
            main = BUTTONS_TEMPLATES['review_form_duty_delete']
            self.extend_keyboard(True, BUTTONS_TEMPLATES['review_form_back_duties'], BUTTONS_TEMPLATES['review_form'])
            return self.build_list(main, unique_args)

        elif view == 'edit_choose':
            unique_args = [{'duty': duty.id} for duty in duties]
            main = BUTTONS_TEMPLATES['review_form_duty_edit']
            self.extend_keyboard(True, BUTTONS_TEMPLATES['review_form_back_duties'], BUTTONS_TEMPLATES['review_form'])
            return self.build_list(main, unique_args)

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """

        view = self.args.get('view')
        duties = self.args.get('duties')
        title = '▪ Обязанности'

        if view == 'list':
            if duties:
                description = '\n❕ Внеси изменения или вернись к анкете.'
                self.build_list_message(title=title,
                                        list_text=[f'{duty.text}' for duty in duties],
                                        description=description)
            return self.MESSAGE

        elif view == 'delete_choose':
            self.build_list_message(title=title,
                                    description='\n❕ Выберите обязанность, которую вы хотите удалить.',
                                    list_text=[f'{duty.text}' for duty in duties])
            return self.MESSAGE

        elif view == 'edit_choose':
            self.build_list_message(title=title,
                                    description='\n❕ Выберите обязанность, которую вы хотите изменить.',
                                    list_text=[f'{duty.text}' for duty in duties])
            return self.MESSAGE

        elif view == 'add':

            text = 'Функционал, который ты выполняешь в ходе своей работы.\n\n <b>Например, я занимаюсь::</b>\nоценкой персонала;\nналаживаю коммуникацию между отделами'
            description = '❕ Напиши все обязанности/.../... одним текстом через «;». Если что-то забудешь, позже можно это исправить:'
            if duties:
                self.build_list_message(title=title,
                                        description=f'\n{description}',
                                        list_text=[f'{duty.text}' for duty in duties])
            else:
                self.build_message(title=title, text=text, description=f'\n{description}')
            return self.MESSAGE


__all__ = ['DutiesForm']
