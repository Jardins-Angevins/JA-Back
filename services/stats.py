import re
import requests

def getDownloadCount():
	# Ask HTML page of the app
	# TODO : For now app isn't published on any store so we use PC[i]'s app stats instead ( another app i developped earlier )
	response = requests.get('https://play.google.com/store/apps/details?id=arcadua.projetcohesion.info')

	# Regex deduced by inspecting html source code of the page
	regex = '<div class="ClM7O">([^>]+)</div><div class="g1rdde">'

	# Scrap the page for the given regex and return only the stat part we are interrested in
	return re.search( regex , response.text ).group(1)