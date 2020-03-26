# multiple-services
This deploy multiple services in google api engine along with back-end using google datastore.

You can deploy this using the follwing command:
```gcloud app deploy blogs/app.yaml rot13/app.yaml user-login/app.yaml```

**You can access the services using the following URLs**:

**blogs** - https://blogs-dot-udacity-tut-271906.appspot.com

The following are the URL handlers :
```webapp2.WSGIApplication([('/blogs/write', MainPage),('/blogs', BlogsHandler)]) ```

**rot13** - https://rot-dot-udacity-tut-271906.appspot.com

The following are the URL handlers :
```webapp2.WSGIApplication([('/rot13', MainPage)])```

**user-login** - https://user-dot-udacity-tut-271906.appspot.com

The following are the URL handlers :
```webapp2.WSGIApplication([('/user_login', MainPage),('/thank_you', ThankyouPage)])```

### Rendering HTML using jinja2
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)
The above function writes out the HTML file in the browser.

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)
The above function takes template and parameters and replacing the variables in HTML with parameters.

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))
This final function combines the other two into one convenient function.
