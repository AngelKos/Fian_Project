#!/usr/bin/env python3
import cgi

form = cgi.FieldStorage()

filedata = request.files['f']

res = open('input.txt', 'w')

res.write(filedata.file.read())

f.close()

print "Content-Type: text/html\n\n";

print "Location: /File_output.html"

