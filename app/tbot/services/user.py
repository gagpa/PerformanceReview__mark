from app.models import UserHistory
from app.db import Session
from sqlalchemy import desc, asc


def save_user_step(request, url, url_type, message):
    if not message or request.args.get('call') and request.args.get('calendar'):
        return
    user = request.user
    history = UserHistory(user=user)
    history.text = url
    args = '/'.join([f'{key}={value}' for key, value in request.args.items()])
    history.args = args
    history.url_type = url_type
    history.message_id = message.message_id
    Session().add(history)
    Session.commit()
    history = Session().query(UserHistory).filter_by(user=user).order_by(asc(UserHistory.id)).all()
    if len(history) > 10:
        for step in history[:-1]:
            Session().delete(step)
        Session.commit()


def get_previous(request):
    user = request.user
    step = Session().query(UserHistory).filter_by(user=user).order_by(desc(UserHistory.id)).first()
    if step.args:
        for arg in step.args.split('/'):
            key, value = arg.split('=')
            left_rim, right_rim = value.find('['), value.find(']')
            value = value[left_rim+1:right_rim].replace("'", '').split(',')
            request.add(key, value)
    return step
