from BaseHTTPServer import HTTPServer
from CGIHTTPServer import CGIHTTPRequestHandler
import time

class Handler(CGIHTTPRequestHandler):
    #cgi_directories = ["/cgi-bin"]
    def do_GET(self):
        try:
            arg = self.path[1:]
            argv = arg.split('/')
            if argv[0]=='set':
                self.set_color(argv)
            else:
                self.serve_index()
        except IOError:
            self.send_error(404, "Page '%s' not found" % self.path)

    def set_color(self, argv):
        import os
        #res = os.system("../ws2812_all.py %s %s %s"%(argv[1], argv[2], argv[3]))
        res = os.system("echo '%s %s %s' > /tmp/rgb"%(argv[1], argv[2], argv[3]))
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write("success: "+str(res))

    def serve_index(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        html = ""
        with open("index.html", mode="r") as f:
            html = f.read()
        self.wfile.write(str(html))



#time.sleep(10)

PORT = 8000

httpd = HTTPServer(("", PORT), Handler)
#print("serving at port", PORT)
httpd.serve_forever()
