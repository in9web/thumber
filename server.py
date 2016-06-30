#coding: utf-8
import os
import sys

import SimpleHTTPServer
import SocketServer

import re

import PIL
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import PIL.JpegImagePlugin

from cStringIO import StringIO

PIL.Image.init() 

def image_generate(image_size = (50, 50), image_color= (210, 210, 210)):
	#init image library

	img = PIL.Image.new("RGB", image_size, image_color)

	path = os.path.realpath(".")

	font = PIL.ImageFont.FreeTypeFont(path + "/Roboto-Light.ttf", 20);

	# ## draw informations
	draw = PIL.ImageDraw.ImageDraw(img)
	draw.font = font

	textsize = draw.textsize(str(image_size))
	draw.text( (image_size[0] / 2 - textsize[0] / 2, image_size[1] / 2 - textsize[1] / 2), str(image_size) )

	s = StringIO()
	img.save(s, "jpeg")
	s.seek(0)
	r = s.read()

	return r

class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

	def do_HEAD(self):
		print "head"

	def do_GET(self):
		path = self.path
		r = re.match("/([0-9]+)[x]([0-9]+)", path)

		if(r):
			width = int(r.group(1));
			height = int(r.group(2));

			response=None

			if(width and height):
				response = image_generate((width, height))
			else:
				response = image_generate()

			self.send_response(200)
			self.send_header('Content-Type', 'image/jpeg')
			self.end_headers()
			self.wfile.write(response)
		else:
			self.send_response(500, "")


PORT =  int(os.environ.get('PORT')) if os.environ.has_key('PORT') else 8000

Handler = MyHandler
httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()


