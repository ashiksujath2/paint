import webapp2
import jinja2
import json
import os

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

from google.appengine.ext import db

class Data(db.Model):
    filename=db.StringProperty()
    imagedata=db.TextProperty()

class MainPage(webapp2.RequestHandler):
    def get(self):
        all_files = db.GqlQuery("SELECT * FROM Data")
        data_dict={}
        for files in all_files:
            data_dict[files.filename]=files.imagedata
        open_file=self.request.path[1:]
        if open_file in data_dict:
            t_values={'files':all_files,'name':open_file,'data':data_dict[open_file]}
        else:
            t_values={'files':all_files,'name':"Untittled",'data':["Not Found"]}
        template = jinja_environment.get_template('paint2.html')
        self.response.out.write(template.render(t_values))
        
    def post(self):
        fname=self.request.get('fnam')
        img=self.request.get('image')
        store = Data(filename=fname,imagedata=img)
        store.put()
        self.redirect("/"+fname)
       

app = webapp2.WSGIApplication([('/.*', MainPage)],debug=True)
