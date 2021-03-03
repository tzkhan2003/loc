
import os
import secrets
from PIL import Image
from flask import url_for, current_app, request
from flask_mail import Message
from flaskblog import mail
import requests
from datetime import datetime, timedelta

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

def save_pro_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/product_pics', picture_fn)

    output_size = (300, 300)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn
def save_post_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/post_pics', picture_fn)

    output_size = (400, 400)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def get_country(ip_address):
    try:
        #response = requests.get("http://ip-api.com/json/24.48.0.1")
        response = requests.get("http://ip-api.com/json/{}".format(ip_address))
        js = response.json()
        country=js["country"]
	#ccd = js["countryCode"]
        rejion = js["regionName"]
        city = js["city"]
        lat = js['lat']
        lon = js["lon"]
        timezone = js["timezone"]
        data = []
        data.append(country)
        data.append(rejion)
        data.append(city)
        data.append(lat)
        data.append(lon)
        data.append(timezone)
	#data.append(ccd)
        return data
    except Exception as e:
        return "Unknown"
#18cc9302abf77cc2f8e7bd751b2858ab
#https://api.openweathermap.org/data/2.5/onecall?lat=45.5808&lon=-73.5825&exclude=current&appid=18cc9302abf77cc2f8e7bd751b2858ab

def call_api(lat , lon):
    key = '18cc9302abf77cc2f8e7bd751b2858ab'
    try:
        response = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&appid={}".format(lat , lon ,key))
        response2 = requests.get("https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}".format(lat , lon ,key))
        response3 = requests.get("http://api.openweathermap.org/data/2.5/air_pollution?lat={}&lon={}&appid={}".format(lat , lon ,key))
        #response = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=45.5808&lon=-73.5825&exclude=current&appid=18cc9302abf77cc2f8e7bd751b2858ab")
        js = response.json()
        js2 = response2.json()
        js3 = response3.json()
        frtemp = int(js2['list'][0]['main']["temp"])-273
        frftemp = int(js2['list'][0]['main']["feels_like"])-273
        frtempmin = int(js2['list'][0]['main']["temp_min"])-273
        frtempmax = int(js2['list'][0]['main']['temp_max'])-273
        frpres = js2['list'][0]['main']["pressure"]
        frhum = js2['list'][0]['main']["humidity"]
        frdis = js2['list'][0]['weather'][0]["description"]
        fricon = "http://openweathermap.org/img/w/"+str(js2['list'][0]['weather'][0]["icon"])+".png"
        frcloud = js2['list'][0]['clouds']["all"]
        frwind = js2['list'][0]['wind']["speed"]
        frwinddeg = js2['list'][0]['wind']["deg"]
        frvis = js2['list'][0]['visibility']


        airv = js3['list'][0]['main']['aqi']
        co = js3['list'][0]['components']['co']
        no = js3['list'][0]['components']['no']
        no2= js3['list'][0]['components']['no2']
        o3 = js3['list'][0]['components']['o3']
        so2 = js3['list'][0]['components']['so2']
        pm2_5 = js3['list'][0]['components']['pm2_5']
        pm10 = js3['list'][0]['components']['pm10']
        nh3 = js3['list'][0]['components']['nh3']


        date = datetime.utcfromtimestamp(int(js['current']['dt'])+int(js['timezone_offset']))
        rise =datetime.utcfromtimestamp(int(js['current']['sunrise'])+int(js['timezone_offset']))
        sett =datetime.utcfromtimestamp(int(js['current']['sunset'])+int(js['timezone_offset']))
        pressure = js['current']['pressure']
        hum = js['current']['humidity']
        dew = int(js['current']['dew_point'])-273
        uvi = js['current']['uvi']
        clouds = js['current']['clouds']
        visibility = js['current']['visibility']
        htemp = int(js['hourly'][0]['temp'])-273
        hftemp = js['hourly'][0]['feels_like']-273
        hpres = js['hourly'][0]['pressure']
        hhum =js['hourly'][0]['humidity']
        hdew = int(js['hourly'][0]['dew_point'])-273
        huv = js['hourly'][0]['uvi']
        hcld = js['hourly'][0]['clouds']
        hvis = js['hourly'][0]['visibility']
        hws = js['hourly'][0]['wind_speed']
        hwd = js['hourly'][0]['wind_deg']
        try:
            altsend=js['alerts'][0]['sender_name']
            altevent=js['alerts'][0]['event']
            altstart=datetime.utcfromtimestamp(int(js['alerts'][0]['start'])+int(js['timezone_offset']))
            altend=datetime.utcfromtimestamp(int(js['alerts'][0]['end'])+int(js['timezone_offset']))
            altdis=js['alerts'][0]['description']
        except Exception as e:
            altsend = 'no alerts currently available'
            altevent ='no alerts currently available'
            altstart = datetime.now()
            altend =datetime.now()
            altdis ='no alerts currently available'
        date2 = date + timedelta(days=1)
        date3 = date2 + timedelta(days=1)
        date4 = date3 + timedelta(days=1)
        date5 = date4 + timedelta(days=1)
        date6 = date5 + timedelta(days=1)
        date7 = date6 + timedelta(days=1)
        temp = int(js['current']['temp'])-273
        ftemp = int(js['current']['feels_like'])-273
        speed = js['current']['wind_speed']
        sdg = js['current']['wind_deg']
        icn = "http://openweathermap.org/img/w/"+str(js['current']['weather'][0]['icon'])+".png"
        weather = []
        weather.append(date)
        weather.append(date2)
        weather.append(date3)
        weather.append(date4)
        weather.append(date5)
        weather.append(date6)
        weather.append(date7)
        weather.append(temp)
        weather.append(ftemp)
        weather.append(speed)
        weather.append(sdg)
        weather.append(icn)
        weather.append(rise)
        weather.append(sett)
        weather.append(pressure)
        weather.append(hum)
        weather.append(dew)
        weather.append(uvi)
        weather.append(clouds)
        weather.append(visibility)
        weather.append(htemp)
        weather.append(hftemp)
        weather.append(hpres)
        weather.append(hhum)
        weather.append(hdew)
        weather.append(huv)
        weather.append(hcld)
        weather.append(hvis)
        weather.append(hws)
        weather.append(hwd)
        weather.append(altsend)
        weather.append(altevent)
        weather.append(altstart)
        weather.append(altend)
        weather.append(altdis)
        weather.append(frtemp) #35
        weather.append(frftemp)
        weather.append(frtempmin)
        weather.append(frtempmax)
        weather.append(frpres)
        weather.append(frhum)
        weather.append(frdis)
        weather.append(fricon)
        weather.append(frcloud)
        weather.append(frwind)
        weather.append(frwinddeg)
        weather.append(frvis)
        weather.append(airv) #47
        weather.append(co)
        weather.append(no)
        weather.append(no2)
        weather.append(o3)
        weather.append(so2)
        weather.append(pm2_5)
        weather.append(pm10)
        weather.append(nh3)

        return weather
    except Exception as e:
        return "Unknown"



def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)
