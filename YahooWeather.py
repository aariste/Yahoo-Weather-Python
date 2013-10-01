from xml.etree.ElementTree import parse
import urllib

YAHOO_NS = 'http://xml.weather.yahoo.com/ns/rss/1.0'
GEO_NS = 'http://www.w3.org/2003/01/geo/wgs84_pos#'

class YahooWeather:
	def __init__(self, woeid, unit):
		self.__woeid = woeid
		self.__unit = unit				
		self.__rss = ''
		
		'''Location'''
		self.__country = ''
		self.__city = ''

		'''Units'''
		self.__temperature_unit = ''
		self.__distance_unit = ''
		self.__pressure_unit = ''
		self.__speed_unit = ''

		'''Wind'''
		self.__wind_chill = ''
		self.__wind_direction = 0
		self.__wind_speed = ''
		self.__cardinal_direction = ''

		'''Atmosphere'''
		self.__humidity = ''
		self.__visibility = ''
		self.__pressure = ''
		self.__rising = ''

		'''Sunrise & Sunset'''
		self.__sunrise = ''
		self.__sunset = ''

		'''Current conditions'''
		self.__condition = ''
		self.__condition_code = ''
		self.__condition_temp = 0
		self.__condition_date = ''

		'''Geo'''
		self.__pub_date = ''
		self.__latitude = 0
		self.__longitude = 0

		'''Prediction'''
		self.__description = ''
		self.__day = []
		self.__date = []
		self.__low = []
		self.__high = []
		self.__text = []
		self.__code = []

		self.__load_data()

	def __load_data(self):
		url = 'http://weather.yahooapis.com/forecastrss?w=' + self.__woeid + '&u=' + self.__unit
		self.__rss = parse(urllib.urlopen(url)).getroot()

		self.__load_location()
		self.__load_units()
		self.__load_wind()
		self.__load_atmosphere()
		self.__load_sun()
		self.__load_geo()
		self.__load_pub_date()
		self.__load_condition()
		self.__load_description()
		self.__load_forecast()
		self.__load_cardinal_direction()

	def __load_location(self):
		for element in self.__rss.findall('channel/{%s}location' % YAHOO_NS):
			self.__country = element.get('country')
			self.__city = element.get('city')

	def __load_units(self):
		for element in self.__rss.findall('channel/{%s}units' % YAHOO_NS):
			self.__temperature_unit = element.get('temperature')
			self.__distance_unit = element.get('distance')
			self.__pressure_unit = element.get('pressure')
			self.__speed_unit = element.get('speed')

	def __load_wind(self):
		for element in self.__rss.findall('channel/{%s}wind' % YAHOO_NS):
			self.__wind_chill = element.get('chill')
			self.__wind_direction = element.get('direction')
			self.__wind_speed = element.get('speed')

	def __load_atmosphere(self):
		for element in self.__rss.findall('channel/{%s}atmosphere' % YAHOO_NS):
			self.__humidity = element.get('humidity')
			self.__visibility = element.get('visibility')
			self.__pressure = element.get('pressure')
			self.__rising = element.get('rising')

	def __load_sun(self):
		for element in self.__rss.findall('channel/{%s}astronomy' % YAHOO_NS):
			self.__sunrise = element.get('sunrise')
			self.__sunset = element.get('sunset')

	def __load_geo(self):
		for element in self.__rss.findall('channel/item/{%s}lat' % GEO_NS):
			self.__latitude = element.text

		for element in self.__rss.findall('channel/item/{%s}long' % GEO_NS):	
			self.__longitude = element.text

	def __load_pub_date(self):
		for element in self.__rss.findall('channel/item/pubDate'):
			self.__pub_date = element.text

	def __load_condition(self):
		for element in self.__rss.findall('channel/item/{%s}condition' % YAHOO_NS):
			self.__condition = element.get('text')
			self.__condition_code = element.get('code')
			self.__condition_temp = element.get('temp')
			self.__condition_date = element.get('date')

	def __load_description(self):
		for element in self.__rss.findall('channel/item/description'):
			self.__description = element.text

	def __load_forecast(self):
		for element in self.__rss.findall('channel/item/{%s}forecast' % YAHOO_NS):
			self.__day.append(element.get('day'))
			self.__date.append(element.get('date'))
			self.__low.append(element.get('low'))
			self.__high.append(element.get('high'))
			self.__text.append(element.get('text'))
			self.__code.append(element.get('code'))

	def __load_cardinal_direction(self):
		wind_direction = float(self.__wind_direction)

		if wind_direction >= 348.75 and wind_direction <= 11.25:
			self.__cardinal_direction = 'N'
		elif wind_direction > 11.25 and wind_direction <= 33.75:
			self.__cardinal_direction = 'NNE'
		elif wind_direction > 33.75 and wind_direction <= 56.25:
			self.__cardinal_direction = 'NE'
		elif wind_direction > 56.25 and wind_direction <= 78.75:
			self.__cardinal_direction = 'ENE'
		elif wind_direction > 78.75 and wind_direction <= 101.25:
			self.__cardinal_direction = 'E'
		elif wind_direction > 101.25 and wind_direction <= 123.75:
			self.__cardinal_direction = 'ESE'
		elif wind_direction > 123.75 and wind_direction <= 146.25:
			self.__cardinal_direction = 'SE'
		elif wind_direction > 146.25 and wind_direction <= 168.75:
			self.__cardinal_direction = 'SSE'
		elif wind_direction > 168.75 and wind_direction <= 191.25:
			self.__cardinal_direction = 'S'
		elif wind_direction > 191.25 and wind_direction <= 213.75:
			self.__cardinal_direction = 'SSO'
		elif wind_direction > 213.75 and wind_direction <= 236.25:
			self.__cardinal_direction = 'SO'
		elif wind_direction > 247.5 and wind_direction <= 270:
			self.__cardinal_direction = 'OSO'
		elif wind_direction > 270 and wind_direction <= 292.5:
			self.__cardinal_direction = 'O'
		elif wind_direction > 292.5 and wind_direction <= 315:
			self.__cardinal_direction = 'ONO'
		elif wind_direction > 315 and wind_direction <= 337.5:
			self.__cardinal_direction = 'NO'
		elif wind_direction > 337.5 and wind_direction <= 348.75:
			self.__cardinal_direction = 'NNO'

		return self.__cardinal_direction

	'''public API'''
	def get_country(self):
		return self.__country

	def get_city(self):
		return self.__city

	def get_temperature_unit(self):
		return self.__temperature_unit

	def get_distance_unit(self):
		return self.__distance_unit

	def get_pressure_unit(self):
		return self.__pressure_unit

	def get_speed_unit(self):
		return self.__speed_unit

	def get_windchill(self):
		return self.__wind_chill

	def get_winddirection(self):
		print self.__wind_direction

	def get_windspeed(self):
		return self.__wind_speed

	def get_cardinal_direction(self):
		return self.__cardinal_direction

	def get_humidity(self):
		return self._humidity

	def get_visibility(self):
		return self.__visibility

	def get_pressure(self):
		return self.__pressure

	def get_rising(self):
		return self.__rising

	def get_sunrise(self):
		return self.__sunrise

	def get_sunset(self):
		return self.__sunset

	def get_latitude(self):
		return self.__latitude

	def get_longitude(self):
		return self.__longitude

	def get_pub_date(self):
		return self.__pub_date

	def get_condition(self):
		return self.__condition

	def get_condition_code(self):
		return self.__condition_code

	def get_condition_temp(self):
		return self.__condition_temp

	def get_condition_date(self):
		return self.__condition_date

	def get_description(self):
		return self.__description

	def get_forecast(self, days):
		days = int(days)

		if days > 4:
			return ''

		return (self.__day[days], self.__date[days], self.__low[days], self.__high[days], self.__text[days], self.__code[days])

	def get_units(self):
		return (self.__temperature_unit, self.__distance_unit, self.__pressure_unit, self.__speed_unit)
		
	def get_all_data(self):
		return (self.__country, self.__city, self.__wind_chill, self.__wind_direction, self.__wind_speed, self.___cardinal_direction, self.__humidity, self.__visibility, self.__pressure, self.__rising, self.___sunrise, self.__sunset)
