import re
from jdatetime import datetime, timedelta
def fa_to_en(text):
    return text.translate(str.maketrans(
        "۰۱۲۳۴۵۶۷۸۹",
        "0123456789"
    ))

def get_digit(string_data):
    string_data = string_data.strip()

    if "صفر" in string_data:
      return 0

    digits = re.sub(r"[^\d]", "", string_data)
    if digits:
      return int(digits)

    return None
  
def get_date(date):
  date = fa_to_en(date.strip())
  now = datetime.now()
  try:
    date = datetime.strptime(date, "%Y/%m/%d")
    return date.strftime("%Y-%m-%d %H:%M:%S")
  except ValueError:
    if "لحظاتی پیش" in date:
      return now.strftime("%Y-%m-%d %H:%M:%S")
    elif "ساعت" in date:
      offset = int(re.sub(r"[^\d]", "", date))
      delta = timedelta(hours=offset)
      return (now - delta).strftime("%Y-%m-%d %H:%M:%S")
    elif "دیروز" in date:
      offset = 1
      return (now - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    elif "روز پیش" in date:
      offset = int(re.sub(r"[^\d]", "", date))
      return (now - timedelta(days=offset)).strftime("%Y-%m-%d %H:%M:%S")
    return now.strftime("%Y-%m-%d %H:%M:%S") 
  
def date_finder(spans):
  date = None
  for span in spans:
    text = span.text.strip()

    if (
      "لحظاتی پیش" in text
      or "دیروز" in text
      or "ساعت پیش" in text
      or "روز پیش" in text
      or re.match(r"^\d{4}/\d{1,2}/\d{1,2}$", fa_to_en(text))
    ):
      date = text
      break
  if date is None:
    date = "لحظاتی پیش"
      
  date = get_date(date)
  return date