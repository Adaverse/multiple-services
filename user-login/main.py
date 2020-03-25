import webapp2
import jinja2
import os
import re

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
	return USER_RE.match(username)

PASSWORD_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
	return PASSWORD_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
	return EMAIL_RE.match(email)

# renders a template
class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	# template is the html file to be rendered
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class ThankyouPage(Handler):
	def get(self):
		self.render('thank_you.html')

class MainPage(Handler):

	# get the variable form the GET operation
	def get(self):
		# get all the get parameters in a string
		print('[INFO]' + ' ' + 'we are in the GET')
		#name = self.request.get('text')
		self.render('base.html',error_username = '', error_password = '', error_email = '')

	def post(self):	
		# flag to decide wether to redirect to the thank you page
		flag = False

		username = self.request.get('username')
		password = self.request.get('password')
		email = self.request.get('email')

		error_username = ''
		error_password = ''
		error_email = ''

		ver_username = valid_username(username)
		if ver_username == None:
			flag = True
			error_username = 'Not a valid username'

		ver_password = valid_password(password)
		if ver_password == None:
			flag = True
			error_password = 'Not a valid password'

		if email:
			ver_email = valid_email(email)
			if ver_email == None:
				error_email = 'Not a valid email'
				flag = True

		print('[INFO]' + ' ' + 'we are in the POST')

		if flag:
			self.render('base.html', error_username = error_username, 
				error_password = error_password, error_email = error_email)
		else:
			self.redirect('/thank_you')

app = webapp2.WSGIApplication([('/user_login', MainPage),('/thank_you', ThankyouPage)], debug = True)
