import requests, pendulum
from utils import slack
from utils.graphql import graphql
import config

active_users_query = """
query($start: timestamptz, $end: timestamptz) {
  user_aggregate(where: {likes: {created_at: {_gte: $start, _lt: $end}}}) {
    aggregate {
      count
    }
  }
}
"""

def get_active_users(date):
  start = date.start_of('week').isoformat()
  end = date.end_of('week').isoformat()

  data = graphql(active_users_query, {'start': start, 'end': end})
  return data.get('data').get("user_aggregate").get("aggregate").get("count")


def format_date(date, date_format):
  return date.format(date_format)

def get_color(progress):
  if progress < 20:
    return "#000000"
  elif progress < 50:
    return "#F44336"
  elif progress < 80:
    return "#FDD835"
  else:
    return "#00C853"

def post_metrics():
  today = pendulum.today()
  active_users = get_active_users(today)
  last_week_users = get_active_users(today.subtract(weeks=1))
  goal = last_week_users + 10
  progress = round(((active_users) / goal) * 100)
  slack_message = [
    {
      "fallback": f"Active users: {active_users}, Goal: {goal}, Progress: {progress}%",
      "color": get_color(progress),
      "pretext": "Good morning! Here are today's metrics.",
      "title": f"Week {format_date(today.start_of('week'), 'Do MMM')} - {format_date(today.end_of('week'), 'Do MMM')}",
      "text": "",
      "fields": [
        {
          "title": "Active This Week",
          "value": active_users,
          "short": True
        },
        {
          "title": "Active Last Week",
          "value": last_week_users,
          "short": True
        },
        {
          "title": "Goal",
          "value": goal,
          "short": True
        },
        {
          "title": "Progress",
          "value": f'{progress}%',
          "short": True
        }
      ],
      "footer": "An active user is a user who has saved an item."
    }
  ]
  return slack.send_message(slack_message, "#metrics" if config.APP_ENV == "production" else "#dev-test")