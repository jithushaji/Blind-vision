import os
from http.server import BaseHTTPRequestHandler, HTTPServer

request = None

class RequestHandler_httpd(BaseHTTPRequestHandler):
  def do_GET(self):
    global request
    #messagetosend = bytes('HELLO',"utf")
    self.send_response(200)
    self.send_header('Content-Type', 'text/plain')
    #self.send_header('Content-Length', len(messagetosend))
    self.end_headers()
    #self.wfile.write(messagetosend)
    request = self.requestline
    request = request[5 : int(len(request)-9)]
    #print(request)
    if request == 'face':
        print('Running face recognition......')
        os.system('python3 Face/Recognize.py')
    if request == 'add':
        print('Adding face......')
        os.system('python3 Face/add_data.py')
    if request == 'text':
        print('Running text recognition......')
        os.system('python3 Text/Text.py')
    if request == 'scene':
        print('Running scene text recognition......')
        os.system('python3 Text/scene_text_detection.py')
    if request == 'object':
        print('Running object recognition.....')
        
    return


server_address_httpd = ('192.168.43.56',8080)
httpd = HTTPServer(server_address_httpd, RequestHandler_httpd)
httpd.serve_forever()

