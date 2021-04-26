from typing import Optional

from telebot.types import InlineKeyboardMarkup

from app.services.form_review.project_comments import ProjectCommentService
from app.tbot.extensions.template import Template
from app.tbot.storages import BUTTONS_TEMPLATES


class ArchiveForm(Template):
    """ Шаблон формы архива """

    def create_markup(self) -> Optional[InlineKeyboardMarkup]:
        """ Создать клавиатуру """
        if self.args.get('models') and self.args.get('review_list'):
            row = BUTTONS_TEMPLATES['get_old_review']
            markup = self.markup_builder.build_list(self.args['models'], row)
            return markup
        elif self.args.get('models') and self.args.get('archive_list'):
            row = BUTTONS_TEMPLATES['get_rapport']
            markup = self.markup_builder.build_list(self.args['models'], row)
            return markup
        elif self.args.get('pk') and self.args.get('choose_rapport'):
            rows = list()
            rows.append([BUTTONS_TEMPLATES['get_hr_rapport'].add(form_id=self.args.get('pk')),
                         BUTTONS_TEMPLATES['get_boss_rapport'].add(form_id=self.args.get('pk'))])
            markup = self.markup_builder.build(*rows)
            return markup

    def create_message(self) -> str:
        """ Вернуть преобразованное сообщение """
        if self.args.get('models') and self.args.get('review_list'):
            title = 'Архив'
            description = 'Выберите номер Review, чтобы посмотреть анкеты:'
            list_data = list()
            for model in self.args["models"]:
                string = f'\nРевью с {model.start_date.date()} по {model.end_date.date()}'
                list_data.append(string)

            message_text = self.message_builder.build_list_message(title=title,
                                                                   description=description,
                                                                   list_data=list_data,
                                                                   )
        elif self.args.get('models') and self.args.get('archive_list'):
            title = 'Архив'
            description = 'Выберите номер анкеты, чтобы сформировать отчет:'
            list_data = list()
            for model in self.args["models"]:
                string = f'{model.user.fullname},\n{model.status.name},\n' \
                         f'{model.review_period.start_date.date()} - {model.review_period.end_date.date()}'
                rating = ProjectCommentService().final_rating(model.id)
                string += f",\nОценка: {rating}\n" if rating else "\n"
                list_data.append(string)

            message_text = self.message_builder.build_list_message(title=title,
                                                                   description=description,
                                                                   list_data=list_data,
                                                                   )
        elif self.args.get('pk') and self.args.get('choose_rapport'):
            text = 'Для кого предназначена выгрузка?'
            message_text = self.message_builder.build_message('', '', text=text)
        else:
            text = 'Нет завершенных Review. ' \
                   'Вы можете остановить его в разделе "Запуск/остановка Review"'
            message_text = self.message_builder.build_message('', '', text=text)

        return message_text


__all__ = ['ArchiveForm']
