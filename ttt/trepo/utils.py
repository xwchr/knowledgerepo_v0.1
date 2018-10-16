def get_formatted_pub_date(datestring,date):

    pubdate = None
    if datestring != '1970/01/01':
        if len(datestring) == 4:
            pubdate = date.strftime('%Y')
        elif len(datestring) == 7:
            pubdate = date.strftime('%b %Y')
        else:
            pubdate = date.strftime('%b %d, %Y')

    return pubdate