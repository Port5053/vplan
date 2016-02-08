import xml.etree.ElementTree as etree
import json

def read_action(element):
	"""Liest eine Veränderung im Lehrer-Vertretungsplan"""

	get = lambda tag: element.find(tag).text
	# Liest den Text aus einem Element
	# raised einen AttributeError falls tag nicht vorhanden.
	
	try:
		old = {
			'subject': get('fach'),
			'teacher': get('lehrer')
		}
		new = {
			'subject': get('vfach'),
			'teacher': get('vlehrer'),
			'room': get('vraum')
		}

		changes = []
		if old['subject'] != new['subject']: changes.append('subject')
		if old['teacher'] != new['teacher']: changes.append('teacher')
		# Am Ende falls Ausfall, werden alle vorherigen Flags überschrieben.
		if new['subject'] == '---': changes = ['cancelled']

		if not changes and not get('info'): changes.append('room')
		else: changes = ['info']
		# not changes besagt, dass changes leer ist, also keine Änderung in Fach und Lehrer. Ist weiterhin
		# keine Info vorhanden ( not get('info') ), dann kann es sich nur um eine Raumänderung handeln

		return {
			'class': get('klasse'),
			'time': get('stunde'),
			'info': get('info'),
			'old': old,
			'new': new,
			'changes': changes
		}

	except AttributeError:
		return None

def convert(xml_content):
	"""Konvertiert einen xml-String in ein dictionary"""
	if not xml_content:
		return None

	try:
		root = etree.fromstring(xml_content)

	except etree.ParseError:
		return None

	events = []
	for element in root.findall('./haupt/aktion'):
		event = read_action(element)

		if event:
			events.append(event)

		else:
			return None

	return {'events': events}
