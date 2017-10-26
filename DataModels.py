from google.appengine.ext import ndb



#simple, contains a booolean and a string
class CheckListItem(ndb.Model):
    title = ndb.StringProperty()
    checked = ndb.BooleanProperty(default=False)
    



class Note(ndb.Model):
        
    #up to 500 characters.
    title = ndb.StringProperty()
    
    #unlimited tedxt.
    
    
    content = ndb.TextProperty(required=True)
    
    #timestamp
    date_created = ndb.DateTimeProperty(auto_now_add=True)
    
    
    #hold some keys for some checklist notes, hence the repeated. 
    checklist_items = ndb.KeyProperty("CheckListItem", repeated=True)

    #get notes
    @classmethod
    def owner_query(cls, parent_key):
        return cls.query(ancestor=parent_key).order(-cls.date_created)

