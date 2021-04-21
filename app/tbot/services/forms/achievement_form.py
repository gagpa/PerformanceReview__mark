from typing import Optional

from telebot.types import InlineKeyboardMarkup

from app.tbot.extensions.template import Template


class AchievementForm(Template):
    """ Шаблон формы достижений """

    def create_markup(self) -> Optional[InlineKeyboardMarkup]:
        """ Создать клавиатуру """
        pass

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """
        view = self.args.get('view')
        achievement = self.args.get('achievement')

        if view == 'edit':
            self.build_message(title='▪️Достижение',
                               description='\nОтправьте в сообщении свои основные достижения и успехи',
                               text=f' -  {achievement.text}')
            return self.MESSAGE


__all__ = ['AchievementForm']
