# /usr/bin/python
# 
# Author:   Miguel Aguilar
# Project:  CDN Download Performance 
# Location: Seattle, WA. Aug 5, 2015
#
# This script has a dependency on the module "requests"
# You can find more information in this site: http://docs.python-requests.org/en/latest/user/install/
# 
# Usage:   python dlperftest.py <URL>
# Example: python dlperftest.py https://www.google.com/images/srpr/logo11w.png

import requests
import sys
import time

from requests import Request, Session

def printHeaders() :
    return

def downloadFile(url) :
    localFilename = url.split('/')[-1]
    directory="./"
    with open(directory + '/' + localFilename, 'wb') as f:
        start = time.time()
        r = requests.get(url, stream=True)
        total_length = int(r.headers.get('content-length'))
        dl=0
        # print r.status_code, type(r.status_code), total_length, r.headers.get('content-length') # debugging line
        
        ### Verify Content-Length header is present, if not, abort script
        if total_length is None: 
            print "No Content-Length header present in the response. Aborting...\n\r"
            # f.write(r.content)
        
        ### Handle situations where we encounter a 302 or 301 for the initial request
        elif r.status_code == 302 | r.status_code== 301 :
            print ("HTTP %s Redirect detected. Unsupported feature. Aborting..." % (r.status_code))
            
        ### Verify file is larger than 101 MegaBytes 
        elif total_length > 104857600+1048576:  
            fileSize = total_length
            rangeVal = int(total_length) - 104857600
            rangeHeader = {"Range": "bytes=" + str(rangeVal) +"-"}
            # rangeHeader = {"Range": "bytes=0-104857599"}
            # print total_length   #debug#
            # print int(total_length)   #debug#
            # print rangeVal   #debug#
            # print rangeHeader   #debug#
            start = time.time()
            r = requests.get(url, stream=True, headers=rangeHeader)
            total_length = int(r.headers.get('content-length'))
            dl = 0
            # print r.request.headers   #debug#
            # print start   #debug#
            print ''
            print ("Downloading URL:\n\r%s" % (url))
            print ("\n\rFile size: %s Mbytes" % (int(fileSize)/(1048576)))
            print ("Range requested: %s-%s (%s Mbytes)\n\r" % (rangeVal, fileSize, (int(total_length)/(1048576))))
            print ("CDN Info: %s\n\rServer: %s" % (r.headers.get('x-cdn-info'), r.headers.get('Server')))
            for chunk in r.iter_content(1024):
                dl += len(chunk)
                speed = ((dl*8)/(1048576))/(time.time() - start)
                done = int((100 * dl) / int(total_length))
                # f.write(chunk)
                sys.stdout.write("\r %s percent done (%s bytes of %s Mbytes) %s Mbps avg. speed" % (done, dl, int(total_length)/(1048576), round(speed, 2)))
                sys.stdout.flush()
                
        ### If file is less than 101 Mbytes it downloads the whole thing
        else:
            start = time.time()
            r = requests.get(url, stream=True, allow_redirects=True)
            total_length = int(r.headers.get('content-length'))
            dl = 0
            # print r.request.headers   #debug#
            # print start   #debug#
            print ''
            print ("Downloading URL:\n\r%s" % (url))
            print ("\r\nCDN Info: %s\n" % (r.headers.get('x-cdn-info')))
            for chunk in r.iter_content(1024):
                dl += len(chunk)
                speed = ((dl*8)/(1048576))/(time.time() - start)
                done = int((100 * dl) / int(total_length))
                # f.write(chunk)
                sys.stdout.write("\r %s percent done (%s bytes of %s Mbytes) %s Mbps avg. speed" % (done, dl, int(total_length)/(1048576), round(speed, 2)))
            
            # for chunk in r.iter_content(1024):
                # dl += len(chunk)
                # #f.write(chunk)
                # done = int((50 * dl) / int(total_length))
                # print "File length: " + total_length 
                # print done
                # sys.stdout.write("\r[%s%s] %s bps" % ('=' * done, ' ' * (50-done), dl/(time.time() - start)))
                # print ''
                
    return (time.time() - start)

def main() :
  if len(sys.argv) > 1 :
        url = sys.argv[1]
  else :
        url = raw_input("Enter a valid URL : ")
        # directory = raw_input("Where would you want to save the file ?")

  time_elapsed = downloadFile(url)
  print ("\n\n\rScript completed in %s seconds" % (("%.2f" % time_elapsed)))
  # print "Time Elapsed: ", 
  # print("%.2f" % time_elapsed), "seconds"


if __name__ == "__main__" :
  main()