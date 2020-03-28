import webapp2
import jinja2
from google.appengine.ext import db

import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), 
	autoescape = True)

# This is the table called Blog
class Blog(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)	
    created = db.DateTimeProperty(auto_now_add = True)

# renders a template
class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	# 
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	# template is the html file to be rendered
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))


class BlogsHandler(Handler):
	def get(self):
		# Query to excess the datastore
		blogs = db.GqlQuery('SELECT * FROM Blog ORDER BY created DESC LIMIT 5')
		self.render('blogs.html', blogs = blogs)

class PermaLinks(Handler):
	def get(self, blog_id):
		blog = Blog.get_by_id(int(blog_id))
		self.render('single_blog.html', blog = blog)	

class MainPage(Handler):
	# renders the html with just one call in both get and post operation
	def render_html(self, subject='',content ='',
	  error_subject = '', error_content = ''):

		# blogs = db.GqlQuery('SELECT * FROM Blog ORDER BY created DESC LIMIT 5')

		print('[INFO]' + ' ' + '.......Im rendering.............')
		self.render('base.html', subject = subject, content = content,
		 error_subject = error_subject, error_content = error_content)

	def get(self):
		# get all the get parameters in a string
		print('[INFO]' + ' ' + 'we are in the GET')
		self.render_html()

	def post(self):
		subject = self.request.get('subject')
		content = self.request.get('content')
		error_content = ''
		error_subject = ''

		print('[INFO]' + ' ' + 'we are in the POST')

		# If nothing entered then just refresh
		if subject and content:
			b = Blog(subject = subject, content = content)
			#self.redirect('/thanks')
			b_key = b.put()

			#self.render_html()
			self.redirect("/blogs/%d" % b_key.id())

		else:
			if subject == u'':
				error_subject = 'Need subject for the blog'
			if content == u'':
				error_content = "Need content for the blog"
			print('printing subject' + " : ", subject)
			self.render_html(subject = subject, content = content,
				error_content = error_content, error_subject = error_subject)

app = webapp2.WSGIApplication([('/blogs/write', MainPage),
	('/blogs', BlogsHandler), 
	('/blogs/(\d+)', PermaLinks)], 
	debug = True)
