import requests
import json



def pobierzpogode(city):
  try:
    api_key = 'Your key goes here'
    r = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}')
    loc_weather = r.content.strip()
    temp,humid,weathertype,rain, city, country = zwroc_elementy_pogody(loc_weather)
    return temp, humid, weathertype, rain, city, country
  except Exception as exp:
    return None



def zwroc_elementy_pogody(wynik_pogody):
  json_pogody = json.loads(wynik_pogody)
  city = json_pogody['name']
  country = json_pogody['sys']['country']
  temp_k = json_pogody["main"]["temp"]
  temp_c = konwertuj_do_c(temp_k)
  humid = json_pogody["main"]["humidity"]
  pressure = json_pogody["main"]["pressure"]
  weathertype = json_pogody["weather"][0]["main"]
  rain = "Rain" if weathertype=="rain" else "no rain"
  return temp_c, humid, weathertype, rain, city, country


def konwertuj_do_c(k):
  return str(round(float(k) - 273.15,2))