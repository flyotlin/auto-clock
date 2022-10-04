"""update.py
Update config.json and crontab by arguments you provided
"""

import argparse
import os
import subprocess


template = "0 {hour} {dates} {month} * python3 {auto_clock} -j {job_name} {type}\n"
auto_clock = "/home/flyotlin/Documents/auto-clock/clock.py"     # change the path as you need
hour_limit = 8  # clock-in hour limit a day


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--job_name", required=True)
    parser.add_argument("-i", "--id", help="humanSys job id")
    parser.add_argument("-m", "--month", required=True, type=int)
    parser.add_argument("-d", "--start_date", required=True, type=int)
    parser.add_argument("-r", "--required_hours", required=True, type=int)

    args = parser.parse_args()
    return args


# TODO: Update config.json by arguments provided
def update_config_job(args):
    pass


def update_crontab(args):
    month = args.month
    start_date = args.start_date
    required_hours = args.required_hours

    pwd = os.path.abspath(os.path.dirname(__file__))
    tmp_crontab = os.path.join(pwd, "tmp_crontab.txt")

    # Duplicate original crontab A
    cron = os.popen(f"crontab -l > {tmp_crontab}")
    cron.read()
    cron.close()

    # Write new crontab rules to A
    with open(tmp_crontab, "a") as cron:
        days_with_limit_hours = required_hours // hour_limit
        hours_left = required_hours % hour_limit

        # Header
        cron.write(f"\n# job for {args.job_name}\n")

        # 8 Hours
        days_str = f"{start_date}-{start_date + days_with_limit_hours - 1}"
        cron.write(template.format(hour=9, dates=days_str, month=month, auto_clock=auto_clock, job_name=args.job_name, type="signin"))
        cron.write(template.format(hour=17, dates=days_str, month=month, auto_clock=auto_clock, job_name=args.job_name, type="signout"))

        # Hours left
        cron.write(template.format(hour=9, dates=str(start_date + days_with_limit_hours), month=month, auto_clock=auto_clock, job_name=args.job_name, type="signin"))
        cron.write(template.format(hour=9+hours_left, dates=str(start_date + days_with_limit_hours), month=month, auto_clock=auto_clock, job_name=args.job_name, type="signout"))

    # Install new crontab rules
    p = subprocess.Popen(f"crontab {tmp_crontab}", stdout=subprocess.PIPE, shell=True)
    rc = p.returncode
    if rc == 0:
        os.remove(tmp_crontab)


if __name__ == "__main__":
    args = parse_args()

    # update_config_job(args)
    update_crontab(args)
