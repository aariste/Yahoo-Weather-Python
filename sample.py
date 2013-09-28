import YahooWeatherAPI

'''Location: Madrid, Spain. Unit: celsius'''
weather = YahooWeatherAPI.YahooWeather('766273', 'c')

'''prints City, current temperature and unit'''
print weather.get_city(), ',', weather.get_condition_temp(), weather.get_temperature_unit()
