import pytz

def convert_to_ist(time):
    ist = pytz.timezone('Asia/Kolkata')
    time = time.replace(tzinfo=pytz.utc).astimezone(ist).strftime('%d-%m-%Y %H:%M')
    return time
