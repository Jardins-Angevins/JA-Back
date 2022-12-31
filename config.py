
import toml

class config:

	data = None

	@staticmethod
	def setup():
		with open('config.toml','r') as conf:
			config.data = toml.loads( ''.join(conf.readlines()) )

	@staticmethod
	def get(path):
		try:

			if config.data is None:
				config.setup()

			res = config.data
			for entry in path.split('.') :
				res = res[entry]
			return res
			
		except KeyError:
			return None

