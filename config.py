
import toml

class config:

	data = None

	@staticmethod
	def setup():
		with open('default-config.toml','r') as conf:
  			config.data = toml.loads( ''.join(conf.readlines()) )

	def get(path):
		try:

			if config.data == None:
				config.setup()

			res = config.data
			for entry in path.split('.') :
				res = res[entry]
			return res
			
		except KeyError:
			return None

