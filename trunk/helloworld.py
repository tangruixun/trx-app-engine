import os
from google.appengine.ext.webapp import template

from google.appengine.ext import db

import cgi
import wsgiref.handlers

from google.appengine.api import users
from google.appengine.ext import webapp

class Greeting(db.Model):
  author = db.UserProperty()
  content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)

class MainPage(webapp.RequestHandler):
#  def get(self):
#    self.response.out.write("""
#      <html>
#        <body>
#          <form action="/sign" method="post">
#            <div><textarea name="content" rows="3" cols="60"></textarea></div>
#            <div><input type="submit" value="Sign Guestbook"></div>
#          </form>
#        </body>
#      </html>""")
##  def get(self):
##    self.response.out.write('<html><body>')

##    greetings = db.GqlQuery("SELECT * FROM Greeting ORDER BY date DESC LIMIT 10")

##    for greeting in greetings:
##      if greeting.author:
##        self.response.out.write('<b>%s</b> wrote:' % greeting.author.nickname())
##      else:
##        self.response.out.write('An anonymous person wrote:')
##      self.response.out.write('<blockquote>%s</blockquote>' %
##                              cgi.escape(greeting.content))

##    # Write the submission form and the footer of the page
##    self.response.out.write("""
##          <form action="/sign" method="post">
##            <div><textarea name="content" rows="3" cols="60"></textarea></div>
##            <div><input type="submit" value="Sign Guestbook"></div>
##          </form>
##        </body>
##      </html>""")


  def get(self):
    greetings_query = Greeting.all().order('-date')
    greetings = greetings_query.fetch(10)

    if users.get_current_user():
      url = users.create_logout_url(self.request.uri)
      url_linktext = 'Logout'
    else:
      url = users.create_login_url(self.request.uri)
      url_linktext = 'Login'

    template_values = {
      'greetings': greetings,
      'url': url,
      'url_linktext': url_linktext,
      }

    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))





class Guestbook(webapp.RequestHandler):
  def post(self):
    greeting = Greeting()

    if users.get_current_user():
      greeting.author = users.get_current_user()

    greeting.content = self.request.get('content')
    greeting.put()

#    self.response.out.write('<html><body>You wrote:<pre>')
#    self.response.out.write(cgi.escape(self.request.get('content')))
#    self.response.out.write('</pre></body></html>')
    self.redirect('/')


def main():
  application = webapp.WSGIApplication(
                                       [('/', MainPage),
                                        ('/sign', Guestbook)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()
