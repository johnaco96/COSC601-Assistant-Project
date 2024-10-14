import python_weather
import asyncio
import assist


async def get_weather(city_name):
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        weather = await client.get(city_name)
        return weather




def parse_command(command):
    if "weather" in command:
        weather_description = asyncio.run(get_weather("Baltimore"))
        query = "System information: " + str(weather_description)
        print(query)
        response = assist.ask_question_memory(query)
        done = assist.TTS(response)
