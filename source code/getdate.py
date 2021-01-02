import datetime
def get_date_list(start,end):
    date_list= []
    date = datetime.datetime.strptime(start,'%Y-%m-%d')
    end = datetime.datetime.strptime(end,'%Y-%m-%d')
    while date <= end:
        date_list.append(date.strftime('%Y-%m-%d'))
        date = date + datetime.timedelta(1)
    return date_list