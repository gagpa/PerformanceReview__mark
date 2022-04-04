import time

import schedule

from app.schedule import active_jobs


def main():
    active_jobs()
    try:
        while True:
            schedule.run_pending()
            time.sleep(5)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
