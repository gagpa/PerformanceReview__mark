"""
Файл с конфигами бота.
"""

import os

TOKEN = os.getenv('TELEBOT_TOKEN')

OBJECT_PER_PAGE = 5

HR_REPORT_TEMPLATE = "templates/hr_report_template.html"
BOSS_REPORT_TEMPLATE = "templates/boss_report_template.html"
