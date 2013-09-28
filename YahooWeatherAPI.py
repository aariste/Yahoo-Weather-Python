from xml.etree.ElementTree import parse
import urllib

YAHOO_NS = 'http://xml.weather.yahoo.com/ns/rss/1.0'
GEO = 'http://www.w3.org/2003/01/geo/wgs84_pos#'

class YahooWeather:
	def __init__(self, woeid, unit):
		self.__woeid = woeid
		self.__unit = unit				
		self.__rss = ''
		
		'''Location'''
		self.__country = ''
		self.__city = ''

		'''Units'''
		self.__temperatureUnit = unit
		self.__distanceUnit = ''
		self.__pressureUnit = ''
		self.__speedUnit = ''

		'''Wind'''
		self.__windChill = ''
		self.__windDirection = 0
		self.__windSpeed = ''
		self.__cardinalDirection = ''

		'''Atmosphere'''
		self.__humidity = ''
		self.__visibility = ''
		self.__pressure = ''
		self.__rising = ''

		'''Sunrise & Sunset'''
		self.__sunrise = ''
		self.__sunset = ''

		self.__pub_date = ''
		self.__geo_latitude = ''
		self.__geo_longitude = ''

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
		self.__load_pub_date()
		self.__load_description()
		self.__load_forecast()
		self.__load_cardinal_direction()

	def __load_location(self):
		for element in self.__rss.findall('channel/{%s}location' % YAHOO_NS):
			self.__country = element.get('country')
			self.__city = element.get('city')

	def __load_units(self):
		for element in self.__rss.findall('channel/{%s}units' % YAHOO_NS):
			self.__distanceUnit = element.get('distance')
			self.__pressureUnit = element.get('pressure')
			self.__speedUnit = element.get('speed')

	def __load_wind(self):
		for element in self.__rss.findall('channel/{%s}wind' % YAHOO_NS):
			self.__windChill = element.get('chill')
			self.__windDirection = element.get('direction')
			self.__windSpeed = element.get('speed')

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

	def load_geo(self):
		for element in self.__rss.iter('channel/item/{%s}' % GEO):
			print element.get('lat')

	def __load_pub_date(self):
		for element in self.__rss.findall('channel/item/pubDate'):
			self.__pub_date = element.text

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
		windDirection = float(self.__windDirection)

		if windDirection >= 348.75 and windDirection <= 11.25:
			self.__cardinalDirection = 'N'
		elif windDirection > 11.25 and windDirection <= 33.75:
			self.__cardinalDirection = 'NNE'
		elif windDirection > 33.75 and windDirection <= 56.25:
			self.__cardinalDirection = 'NE'
		elif windDirection > 56.25 and windDirection <= 78.75:
			self.__cardinalDirection = 'ENE'
		elif windDirection > 78.75 and windDirection <= 101.25:
			self.__cardinalDirection = 'E'
		elif windDirection > 101.25 and windDirection <= 123.75:
			self.__cardinalDirection = 'ESE'
		elif windDirection > 123.75 and windDirection <= 146.25:
			self.__cardinalDirection = 'SE'
		elif windDirection > 146.25 and windDirection <= 168.75:
			self.__cardinalDirection = 'SSE'
		elif windDirection > 168.75 and windDirection <= 191.25:
			self.__cardinalDirection = 'S'
		elif windDirection > 191.25 and windDirection <= 213.75:
			self.__cardinalDirection = 'SSO'
		elif windDirection > 213.75 and windDirection <= 236.25:
			self.__cardinalDirection = 'SO'
		elif windDirection > 247.5 and windDirection <= 270:
			self.__cardinalDirection = 'OSO'
		elif windDirection > 270 and windDirection <= 292.5:
			self.__cardinalDirection = 'O'
		elif windDirection > 292.5 and windDirection <= 315:
			self.__cardinalDirection = 'ONO'
		elif windDirection > 315 and windDirection <= 337.5:
			self.__cardinalDirection = 'NO'
		elif windDirection > 337.5 and windDirection <= 348.75:
			self.__cardinalDirection = 'NNO'

		return self.__cardinalDirection

	'''public API'''
	def get_country(self):
		return self.__country

	def get_city(self):
		return self.__city

	def get_temperature_unit(self):
		return self.__temperatureUnit

	def get_distance_unit(self):
		return self.__distanceUnit

	def get_pressure_unit(self):
		return self.__pressureUnit

	def get_speed_unit(self):
		return self.__speedUnit

	def get_windchill(self):
		return self.__windChill

	def get_winddirection(self):
		print self.__windDirection

	def get_windspeed(self):
		return self.__windSpeed

	def get_cardinal_direction(self):
		return self.__cardinalDirection

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

	def get_pub_date(self):
		return self.__pub_date

	def get_description(self):
		return self.__description

	def get_forecast(self, days):
		days = int(days)

		if days > 4:
			return ''

		return (self.__day[days], self.__date[days], self.__low[days], self.__high[days], self.__text[days], self.__code[days])

	def get_units(self):
		return (self.__temperatureUnit, self.__distanceUnit, self.__pressureUnit, self.__speedUnit)

	def get_all_data(self):
		return (self.__country, self.__city, self.__windChill, self.__windDirection, self.__windSpeed, self.___cardinalDirection, self.__humidity, self.__visibility, self.__pressure, self.__rising, self.___sunrise, self.__sunset)
	