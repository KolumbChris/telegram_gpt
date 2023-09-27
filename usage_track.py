import os.path
import pathlib
import json
from datetime import date


def year_month(date):
    # extract string of year-month from date, eg: '2023-03'
    return str(date)[:7]


class UsageTrack:

    def __init__(self, user_id, user_name, logs_dir="usage_logs"):
        self.user_id = user_id
        self.logs_dir = logs_dir
        # path to usage file of given user
        self.user_file = f"{logs_dir}/{user_id}.json"

        if os.path.isfile(self.user_file):
            with open(self.user_file, "r") as file:
                self.usage = json.load(file)
        else:
            # ensure directory exists
            pathlib.Path(logs_dir).mkdir(exist_ok=True)
            # create new dictionary for this user
            self.usage = {
                "user_name": user_name,
                "current_cost": {"day": 0.0, "month": 0.0, "last_update": str(date.today())},
                "usage_history": {"chat_tokens": {}, "transcription_seconds": {}, "number_images": {}}
            }

    def get_current_cost(self):
        today = date.today()
        last_update = date.fromisoformat(self.usage["current_cost"]["last_update"])
        if today == last_update:
            cost_day = self.usage["current_cost"]["day"]
            cost_month = self.usage["current_cost"]["month"]
        else:
            cost_day = 0.0
            if today.month == last_update.month:
                cost_month = self.usage["current_cost"]["month"]
            else:
                cost_month = 0.0
        return round(cost_day, 3), round(cost_month, 3)
