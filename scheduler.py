import time

import schedule

from app.schedule import active_jobs


def main():
    active_jobs()
    while True:
        schedule.run_pending()
        time.sleep(5)


if __name__ == '__main__':
    main()
