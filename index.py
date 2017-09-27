import SimpleHTTPServer
import SocketServer
import requests
from datetime import datetime
import os
import logging

redir = os.environ['REDIRECT']
zapier= os.environ['ZAPIER_HOOK']


class myHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
   def do_GET(self):
       print self.path
       now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
       requests.post(zapier, json={"IP":self.client_address[0], "date": now, "type": self.path, "browser":self.headers.get('User-Agent')})
       self.send_response(302)
       #new_path = '%s%s'%(redir, self.path)
       new_path = redir
       self.send_header('Location', new_path)
       self.end_headers()

PORT = os.environ['PORT']
handler = SocketServer.TCPServer(("", int(PORT)), myHandler)
print "serving at port "+ PORT
handler.serve_forever()
