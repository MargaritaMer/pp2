import datetime
now = datetime.datetime.now()
one = datetime.timedelta(days=1)
print("Yesterday",now-one)
print("Today",now)
print("Tomorrow",now+one)