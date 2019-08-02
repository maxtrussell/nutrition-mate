from datetime import datetime

def toDate(dateString):
    return datetime.strptime(dateString, "%Y-%m-%d").date()

def toTime(timeString):
    return datetime.strptime(timeString, "%Y-%m-%d %H:%M:%S")
