from pyramid.security import remember, forget
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, view_defaults

from .group_finder import can_read, can_edit


@view_defaults(route_name='home', renderer='templates/home.pt')
class HomeView:
	""" Startadresse "/". (Eigentlich Login) """
	def __init__(self, request):
		self.request = request

	def redirect(self, route_name, headers=None):
		# erspart Tipparbeit
		return HTTPFound(location=self.request.route_path(route_name), headers=headers)

	@view_config(request_method='GET')
	def view_start(self):
		"""Handelt einen GET-Request, wie z. B. Redirects"""

		# Falls in der URL der Query ?logout war, wird der User über forget abgemeldet, 
		# und zur Start(Anmelde)-Seite umgeleitet

		# Die Permission wird aber nicht zurückgesetzt...
		# auch nach dem Abmelden kann man noch /schedule ohne Passwort eingeben

		# // sollte es aber? wenn man jemand anderen an den rechner lassen will bzw. dieser öffentlich ist sollte es aus sicherheitsgründen komplett abmelden
		if 'logout' in self.request.params:
			headers = forget(self.request)
			return self.redirect('home', headers)
		
		# Redirects von der Startseite von schon angemeldeten Schülern
		if self.request.has_permission('read'):
			return self.redirect('schedule')
		
		if self.request.has_permission('edit'):
			return self.redirect('edit')

		# Falls keine der obigen Bedingungen erfüllt, kann es sich nur um eine
		# erstmalige Anmeldung handeln. Also noch nichts falsch angezeigt.
		return {'wrong_pwd': False}

	@view_config(request_method='POST')
	def answer_post(self):
		pwd_hash = self.request.params['hash']
		headers = None

		if can_read(pwd_hash):
			headers = remember(self.request, pwd_hash)
			return self.redirect('schedule', headers)

		if can_edit(pwd_hash):
			headers = remember(self.request, pwd_hash)
			return self.redirect('edit', headers)

		# wenn keines der obigen Bedingungen erfüllt, muss das Passwort
		# falsch gewesen sein.
		return {'wrong_pwd': True}

# Ich weiß nicht, wo ich das sonst hinschreiben soll:
#	Wir sollten in der Server-Dateien eine Offline-Kopie von jQuery haben, damit ich mich auch im Internat anmelden kann.
#	Aktuell gibt es keine JS-Überprüfung, ob $ erfolgreich geladen worden ist.