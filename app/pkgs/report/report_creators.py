from abc import ABC

from jinja2 import FileSystemLoader, Environment
from weasyprint import HTML

from app.schemas import FormFrame


class ReportCreator(ABC):
    _path: str = ''
    _filename_template = '{consumer}_report_{username}.pdf'
    _consumer = 'default'

    def __init__(self, form: FormFrame):
        self.form = form

    def create(self):
        filename = self._filename_template.format(consumer=self._consumer,
                                                  username=self.form.author.username,
                                                  )
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template(self._path)
        html_out = template.render(self.form)
        HTML(string=html_out).write_pdf(filename)
        return filename


class ReportCreatorForLead(ReportCreator):
    _path: str = 'templates/lead/template.html'
    _consumer = 'lead'


class ReportCreatorForHR(ReportCreator):
    _path: str = 'templates/hr/template.html'
    _consumer = 'hr'
