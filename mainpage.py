
import webapp2

import os
import jinja2

from google.appengine.api import users
from google.appengine.ext import ndb  

from DataModels import Note
from DataModels import CheckListItem


#setup jinja
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


#application routes, add more as necessary.
routes = [
    ('/', 'mainpage.MainPage'),
]


class MainPage(webapp2.RequestHandler):

     def render_template(self, template_name, context=None):
           if context is None:
               context = {}
           
           #retrieve the data.    
           user = users.get_current_user()
           #gen key
           ancestor_key = ndb.Key("User", user.nickname())
           #get a query setup
           qry = Note.owner_query(ancestor_key)
           
           
           
           #a mapping, notes is the key, qry.fetch() is the value, coresponds to mainpage notes
           context['notes'] = qry.fetch()
        
        
           template = jinja_env.get_template(template_name)
           return template.render(context)  
    
    
    
    
     def get(self):
      
            user = users.get_current_user()
            
            #if the user is logged in
            if user is not None:
              
             
                
                #get the logout url and return to homepage when done.
              logout_url = users.create_logout_url(self.request.uri)
              #get the file
              template = jinja_env.get_template('mainpage.html')
              #dictionary mapping to {{keyword}} variable in html
              
              #add info the the html page.
              template_context = { 'user': user.nickname() ,'logout_url': logout_url,}
              self.response.out.write( self.render_template(template,template_context)  )

      
      
            #the user is NOT logged in.
            else:
           #the user must login here
                  
                  #get the url of the login page, the parameter represents where to redirect on successful login
                  login_url = users.create_login_url(self.request.uri)
                  self.redirect(login_url) 
          
          
             
      #handle new note.
     def post(self):
        user = users.get_current_user()
        if user is None:
            self.error(401)
            
            
        logout_url = users.create_logout_url(self.request.uri)
        
        
        self.create_note(user)
        
        
        template_context = {
        'user': user.nickname(),
        'logout_url': logout_url,
        
        }      
        self.response.out.write(self.render_template('mainpage.html', template_context))
           
     
     #assure success of all operations.
     @ndb.transactional
     def create_note(self, user):
         note = Note(parent=ndb.Key("User", user.nickname()),
                   title=self.request.get('title'),
                   content=self.request.get('content'))
         note.put()
        
         item_titles = self.request.get('checklist_items').split(',')
         for item_title in item_titles:
           item = CheckListItem(parent=note.key, title=item_title)
           item.put()
           note.checklist_items.append(item.key)
         note.put()
    
    

#app defined by routes and turn off debug in production! Its only for errors.
application = webapp2.WSGIApplication(routes, debug=True)


