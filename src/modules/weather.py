import requests

def get_weather_forecast(api_key):
    cities = [('Sunland,CA', 'US'), ('Valencia,CA', 'US'), ('Yerevan', 'AM')]
    current_weather_strs = []

    for city, country in cities:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={api_key}&units=metric'
        response = requests.get(url)

        print(f'Response status code: {response.status_code}')
        print(f'Response content: {response.content}')

        if response.status_code == 200:
            data = response.json()

            temperature = data.get('main', {}).get('temp')
            description = data.get('weather', [{}])[0].get('description')
            if temperature is not None and description is not None:
                formatted_temp = f'{temperature}°C'
                formatted_weather = f'{city} - {description}, {formatted_temp}'
                current_weather_strs.append(formatted_weather)
            else:
                print(f'Error retrieving weather data for {city}: Incomplete response')
        else:
            print(f'Error retrieving weather data for {city}: {response.status_code} - {response.text}')

    return '\n'.join(current_weather_strs)

# Example usage
weather_forecast = get_weather_forecast('65f6302c3f563782488f7dc78cf9a596')
