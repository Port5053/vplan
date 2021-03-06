from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from .permissions import RootFactory, get_group


timeout = 1000

def main(global_config, **settings):
	""" This function returns a Pyramid WSGI application.
	"""
	config = Configurator(settings=settings, root_factory=RootFactory)
	config.include('pyramid_chameleon')

	authn_policy = AuthTktAuthenticationPolicy(settings['vp.secret'], callback=get_group, hashalg='sha512', timeout=timeout)
	authz_policy = ACLAuthorizationPolicy()
	config.set_authentication_policy(authn_policy)
	config.set_authorization_policy(authz_policy)

	config.add_route('login', '/')
	config.add_route('upload', '/upload')
	config.add_route('schedule', '/schedule')
	config.add_route('eastereggs', '/eastereggs/{hash}')
	config.add_route('ea_empty', '/eastereggs')

	config.add_static_view('static', 'vp:static')
	config.scan()

	return config.make_wsgi_app()
