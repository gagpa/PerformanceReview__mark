from app.db import Session
from app.models import Form
from app.pkgs.report import report_creators, create_form_frame
from zipfile import ZipFile
import os

if __name__ == '__main__':
    with ZipFile('reports.zip', 'w') as zip_file:
        i = 0
        for form in Session().query(Form).all():
            frame = create_form_frame(form)
            lead = report_creators.ReportCreatorForLead(frame).create()
            hr = report_creators.ReportCreatorForHR(frame).create()
            zip_file.write(lead)
            zip_file.write(hr)
            os.remove(lead)
            os.remove(hr)
            i += 1
            print(i)
    # form = Session().query(Form).all()[10]
    # frame = create_form_frame(form)
    # lead = report_creators.ReportCreatorForLead(frame).create()
    # hr = report_creators.ReportCreatorForHR(frame).create()
