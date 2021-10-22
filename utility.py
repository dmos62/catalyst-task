import datetime

def get_today():
    return datetime.date.today()

def to_iso8601(date):
    return date.isoformat()
