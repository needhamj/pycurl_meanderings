#!/usr/bin/python
from StringIO import StringIO
from datetime import datetime
import pycurl
import time
import signal
import sys


class TestConnection(object):

    def __init__(self):
        self.number_of_RTTs = 0.0
        self.avg_RTT = 0.0
        self.goodput = 0

    def signal_handler(self, signal, frame):
        if self.number_of_RTTs == 0:
            output_string = "no data been passed back yet"
        else:
            output_string  = "Average RTT: %s, Goodput: %s" % (
                self.avg_RTT / self.number_of_RTTs,
                self.goodput / self.number_of_RTTs,
            )
        print(output_string)
        sys.exit(0)
    #signal.pause()


    def execute_connection(self):
        buffer = StringIO()
        send_data = "1"*1000 # should be represented as 1000 bytes in the packet
        # Set up curl
        a=pycurl.Curl()
        a.setopt(pycurl.VERBOSE, 1)
        a.setopt(pycurl.URL, "http://authenticationtest.herokuapp.com/login/")
        a.setopt(pycurl.USERPWD, "testuser:54321password12345")
        a.setopt(pycurl.WRITEFUNCTION, buffer.write)
        a.setopt(pycurl.HTTPPOST, [(
            'fileupload', (
            a.FORM_BUFFER, 'file.txt',
            a.FORM_BUFFERPTR, send_data,
            ))
        ])
        # Authentication
        a.perform()

        # Send packet
        # Packet can be modelled to contain 1000 bytes of useful data.

        for i in range (1,10):
            time.sleep(3)
            self.number_of_RTTs += 1
            t = datetime.now()
            a.perform()

            # See when it comes back.
            t = datetime.now() - t
            self.avg_RTT += t.total_seconds()
            self.goodput = 1000 / t.total_seconds()


if __name__ == "__main__":
    t = TestConnection()
    signal.signal(signal.SIGINT, t.signal_handler)
    t.execute_connection()
