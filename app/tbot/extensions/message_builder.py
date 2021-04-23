from typing import Optional


class MessageDecorator:
    """ Оформлятор сообщений """
    __DECOR = {
        'title': '<b>{}</b>',
        'description': '<i>{}</i>',
        'text': '{}',
    }

    def do_title(self, title: str):
        """ Оформить заголовок """
        if title:
            title = self.__DECOR['title'].format(title)
        return title

    def do_description(self, description: str):
        """ Оформить описание """
        if description:
            description = self.__DECOR['description'].format(description)
        return description

    def do_text(self, text: str):
        """ Оформить текст """
        if text:
            text = self.__DECOR['text'].format(text)
        return text

    def do_list(self, items: Optional[list]):
        """ Оформить список """
        if items:
            # Функция для выявления последнего элемента списка
            last_item = len(items) - 1

            def is_not_last(item):
                return item < last_item

            # Сборка списка
            list_text = ''
            for i, data in enumerate(items):
                list_text += f'{i + 1}. {data}'
                # Если это не последний элемент, то вставляет перенос строки

                if is_not_last(item=i):
                    list_text += '\n'
        else:
            list_text = 'Список пустой'
        return list_text


class MessageBuilder(MessageDecorator):
    """ Строитель сообщений от телеграмм бота """
    __LIST_TEMPLATE = '{title}\n{list_data}\n{description}\n'
    __DEFAULT_TEMPLATE = '{title}\n{text}\n{description}\n'

    def build_list_message(self, title: str = None, description: Optional[str] = None, list_data: Optional[list] = None):
        """ Построить сообщения списка данных """
        template = self.__LIST_TEMPLATE
        title = self.do_title(title)
        description = self.do_description(description)
        list_data = self.do_list(list_data)
        if not title:
            template = template.replace('{title}\n', '')
        if not description:
            template = template.replace('\n{description}', '')
        if not list_data:
            template = template.replace('\n{text}', '')
        message = template.format(title=title, description=description, list_data=list_data)
        return message

    def build_message(self, title: str = None, description: Optional[str] = None, text: Optional[str] = None):
        """ Посторить сообщение """
        template = self.__DEFAULT_TEMPLATE
        title = self.do_title(title)
        description = self.do_description(description)
        data = self.do_text(text)
        if not title:
            template = template.replace('{title}', '')
        if not description:
            template = template.replace('\n{description}', '')
        if not data:
            template = template.replace('\n{text}', '')
        message = template.format(title=title, description=description, text=data)
        return message


__all__ = ['MessageBuilder']
