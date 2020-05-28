#!/usr/bin/env python
import os
import sys
from pwn import *

port = 80
port1 = 443
subdomains = []
printable = []
errors = ["Double check the URL or ","404 Not Found","The feed has not been found.", "The thing you were looking for is no longer here, or never was","We could not find what you're looking for.", "No settings were found for this company:", "No such app", "is not a registered InCloud YouTrack", "404 Web Site not found", "Project doesnt exist... yet!", "project not found", "Whatever you were looking for doesn't currently exist at this address", "This UserVoice subdomain is currently available!", "Do you want to register", "But if you're looking to build your own website,", "This public status page <b>does not seem to exist</b>.", "The gods are wise", "Double check the URL or ","NoSuchBucket", "There isn\'t a GitHub Pages site here", "//www.herokucdn.com/error-pages/no-such-app.html", "Project doesnt exist... yet", 'The specified bucket does not exist', 'Repository not found', '404 Not Found', 'Fastly error: unknown domain', 'The feed has not been found', 'The thing you were looking for is no longer here, or never was', "There isn't a Github Pages site here", "We could not find what you're looking for", 'No settings were found for this company', 'No such app', "Uh oh. That page doesn't exist", "is not a registered InCloud YouTrack", "No Site For Domain", "It looks like you may have taken a wrong turn somewhere. Don't worry...it happens to all of us", "Unrecognized domain", "404 error unknown site!", "Project doesnt exist... yet!", "Sorry, this shop is currently unavailable", "page not found", "project not found", "Whatever you were looking for doesn't currently exist at this address", "Please renew your subscription", "page not found", "This UserVoice subdomain is currently available", "404 Page Not Found", "Do you want to register *.wordpress.com?"]
vuln = ['s3', 'campaign', 'cargo', 'github', 'fastly', 'feedpress', 'ghost', 'juice', 'scout', 'heroku', 'intercom', 'jetbrains', 'kinsta', 'launchrock', 'mashery', 'pantheon', 'readme', 'shopify', 'strikingly', 'surge', 'tumblr', 'tilda', 'uptimerobot', 'uservoice', 'webflow', 'wordpress', 'azure']
file = sys.argv[1]
cnames = []
for file in files:
    fopen = open(file, 'r')
    for line in fopen:
        for word in vuln:
	    if word in line.strip().lower() and 'CNAME' in line.strip():
                cnames.append(line.strip())
		
fopen.close()
for line in cnames:
    k = line.split()
    l = len(k[0])-1
    str = k[0]
    subdomain = str[0:l]
    print subdomain
    subdomains.append(subdomain)

for host in subdomains:
    r = remote(host, port, ssl=False, timeout=25)
    r.send("GET / HTTP/1.1\r\nHost: " + host + "\r\n\r\n")
    data = r.recv()
    r.close()
    if "200 OK" not in data:
        r = remote(host, port1, ssl=True, timeout=25)
	r.send("GET / HTTP/1.1\r\nHost: " + host + "\r\n\r\n")
	data = r.recv()
	r.close()
    for error in errors:
        if error in data:
	    printable.append(host)

if not printable:
    print "Subdomain Takeover not possible"
else:
    print "Subdomain Takeover can be possible: \n"
    for i in printable:
        print i


