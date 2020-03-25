import webapp2
import jinja2
import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

def shifttext(s, shift = 13):
	strs = 'abcdefghijklmnopqrstuvwxyz'  
	inp = s
	data = []
	for i in inp:                     #iterate over the text not some list
		if i.strip() and i in strs:                 # if the char is not a space ""  
			data.append(strs[(strs.index(i) + shift) % 26])    
		else:
			data.append(i)           #if space the simply append it to data
	output = ''.join(data)
	return output

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



class MainPage(Handler):
	# get the variable form the GET operation
	def get(self):
		# get all the get parameters in a string
		print('[INFO]' + ' ' + 'we are in the GET')
		name = self.request.get('text')
		self.render('base.html', texts = name)
	def post(self):
		name = self.request.get('text')
		print('[INFO]' + ' ' + 'we are in the POST')
		rev = ''
		if name:
			rev = shifttext(name)
		self.render('base.html', texts = rev)

app = webapp2.WSGIApplication([('/rot13', MainPage)], debug = True)
