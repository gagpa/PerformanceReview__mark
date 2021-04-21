from telebot.types import InlineKeyboardMarkup

from app.tbot.extensions.template import Template
from app.tbot.storages import BUTTONS_TEMPLATES


class AchievementsForm(Template):
    """ Шаблон формы достижений """

    def create_markup(self) -> InlineKeyboardMarkup:
        """ Создать клавиатуру """
        view = self.args.get('view')
        achievements = self.args.get('achievements')

        if view == 'list':
            self.extend_keyboard(False, BUTTONS_TEMPLATES['review_form_achievements_add'])
            if achievements:
                self.extend_keyboard(True, BUTTONS_TEMPLATES['review_form_achievements_edit_choose'],
                                     BUTTONS_TEMPLATES['review_form_achievements_delete_choose'])
            self.extend_keyboard(True, BUTTONS_TEMPLATES['review_form'])
            return self.build()

        elif view == 'delete_choose':
            unique_args = [{'achievement': achievement.id} for achievement in achievements]
            main = BUTTONS_TEMPLATES['review_form_achievement_delete']
            return self.build_list(main, unique_args)

        elif view == 'edit_choose':
            unique_args = [{'achievement': achievement.id} for achievement in achievements]
            main = BUTTONS_TEMPLATES['review_form_achievement_edit']
            return self.build_list(main, unique_args)

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """
        view = self.args.get('view')
        achievements = self.args.get('achievements')
        title = '▪️Достижения'

        if view == 'list':
            description = 'Факты, которые ты считаешь своими основными достижениями и успехами'
            if achievements:
                self.build_list_message(title=title,
                                        description=f'\n{description}',
                                        list_text=[f'{achievement.text}' for achievement in achievements])
            else:
                self.build_message(title=title, description=description)
            return self.MESSAGE

        elif view == 'delete_choose':
            self.build_list_message(title=title,
                                    description='\nВыберите достижение, которое вы хотите удалить',
                                    list_text=[f'{achievement.text}' for achievement in achievements])
            return self.MESSAGE

        elif view == 'edit_choose':
            self.build_list_message(title=title,
                                    description='\nВыберите достижение, которое вы хотите изменить',
                                    list_text=[f'{achievement.text}' for achievement in achievements])
            return self.MESSAGE

        elif view == 'add':
            description = 'Отправьте в сообщении свои основные достижения и успехи'
            if achievements:
                self.build_list_message(title=title,
                                        description=f'\n{description}',
                                        list_text=[f'{achievement.text}' for achievement in achievements])
            else:
                self.build_message(title=title, description=description)
            return self.MESSAGE


__all__ = ['AchievementsForm']
