import schedule

from . import jobs


def active_jobs():
    """Активировать задачи"""
    schedule.every(5).seconds.do(jobs.review.send_to_archive)
