import config
import requests
from twilio.rest import Client

def get_coordinates(zip_code="94132", 
                    country_code="US", 
                    api_key=config.weather_api_key):
    return requests.get(f"http://api.openweathermap.org/geo/1.0/zip?zip={zip_code},{country_code}&appid={api_key}").json()

def get_data(lat="37.7211", lon="-122.4754", apiKey=config.weather_api_key):
    return requests.get(f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={apiKey}").json()

def send_notifications(time, temp, weather): 
    print("called")
    account_sid = config.twilio_account_sid
    auth_token = config.twilio_auth_token
    client = Client(account_sid, auth_token)
    
    client.messages.create(
        from_='whatsapp:+14155238886',
        body= f"Weather Forecast by Monkey Lee:\nTime: {time}\nTemp: {temp}\nWeather: {weather}",
        to='whatsapp:+15104537036'
    )

def main():
    coordinates = get_coordinates()
    forecast_list = get_data(coordinates['lat'], coordinates['lon'])['list']
    for forecast in forecast_list[:4]:
        time = forecast['dt_txt']
        temp = "{:.2f}".format(forecast['main']['temp'])
        weather_id = forecast['weather'][0]['id']
        if weather_id < 800 or temp < 10:
            weather = forecast['weather'][0]['main']
            send_notifications(time, temp, weather)
            break
        

if __name__ == "__main__":
    main()
