import SimpleHTTPServer
import SocketServer
import requests
from datetime import datetime
import os
redir = os.environ['REDIRECT']
zapier= os.environ['ZAPIER_HOOK']


class myHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
   def do_GET(self):
       print self.path
       now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
       requests.post(zapier, json={"IP":self.client_address[0], "date": now, "type": self.path})
       self.send_response(303)
       #new_path = '%s%s'%(redir, self.path)
       new_path = redir
       self.send_header('Location', new_path)
       self.end_headers()

PORT = 8000
handler = SocketServer.TCPServer(("", PORT), myHandler)
print "serving at port 8000"
handler.serve_forever()
