from telebot.types import InlineKeyboardMarkup

from app.tbot.extensions.template import Template
from app.tbot.storages import BUTTONS_TEMPLATES


class FailsForm(Template):
    """ Шаблон формы провалов """

    def create_markup(self) -> InlineKeyboardMarkup:
        """ Создать клавиатуру """
        view = self.args.get('view')
        fails = self.args.get('fails')

        if view == 'list':
            self.extend_keyboard(False, BUTTONS_TEMPLATES['review_form_fails_add'])
            if fails:
                self.extend_keyboard(True, BUTTONS_TEMPLATES['review_form_fails_edit_choose'],
                                     BUTTONS_TEMPLATES['review_form_fails_delete_choose'])
            self.extend_keyboard(True, BUTTONS_TEMPLATES['review_form'])
            return self.build()

        elif view == 'delete_choose':
            unique_args = [{'fail': fail.id} for fail in fails]
            main = BUTTONS_TEMPLATES['review_form_fail_delete']
            self.extend_keyboard(True, BUTTONS_TEMPLATES['review_form_back_fails'], BUTTONS_TEMPLATES['review_form'])
            return self.build_list(main, unique_args)

        elif view == 'edit_choose':
            unique_args = [{'fail': fail.id} for fail in fails]
            main = BUTTONS_TEMPLATES['review_form_fail_edit']
            self.extend_keyboard(True, BUTTONS_TEMPLATES['review_form_back_fails'], BUTTONS_TEMPLATES['review_form'])
            return self.build_list(main, unique_args)

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """
        view = self.args.get('view')
        fails = self.args.get('fails')
        title = '▪️Провалы'

        if view == 'list':

            if fails:
                self.build_message(title=title,
                                   description='Факты, которые ты считаешь своими основными провалами. ' \
                                               '\nЧем вы сами недовольны, и что хотели бы исправить и' \
                                               ' улучшить в будущем.')

                description = '\n❕ Нажми кнопку “добавить” и перечисли свои провалы – через «;». Если что-то забудешь, позже можно это исправить.'
                self.build_list_message(description=description,
                                        list_text=[f'{fail.text}' for fail in fails])
            return self.MESSAGE

        elif view == 'delete_choose':
            self.build_list_message(title=title,
                                    description='\n❕ Выберите провал, которое вы хотите удалить.',
                                    list_text=[f'{fail.text}' for fail in fails])
            return self.MESSAGE

        elif view == 'edit_choose':
            self.build_list_message(title=title,
                                    description='\n❕ Выберите провал, которое вы хотите изменить.',
                                    list_text=[f'{fail.text}' for fail in fails])
            return self.MESSAGE

        elif view == 'add':
            description = '❕ Перечисли свои провалы – через «;». Если что-то забудешь, можно будет исправить это позже.'
            self.build_message(title=title,
                               description='Напиши все провалы одним текстом через «;». Если что-то забудешь, позже можно это исправить:')
            if fails:
                self.build_list_message(description=f'\n{description}',
                                        list_text=[f'{fail.text}' for fail in fails])
            else:
                self.build_message(description=description)
            return self.MESSAGE


__all__ = ['FailsForm']
