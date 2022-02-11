from shutil import ExecError
import redis
import logging
import traceback

# try :
#     client = redis.Redis(host='localhost', port=6379)
# except Exception as e :
#     print("something went wrong see error below")
#     logging.error(traceback.format_exc())


class urlshortener():
    client = None
    base_url = 'https://urlshort.ly'

    def __init__(self):
        try:
            client = redis.Redis(host='localhost', port=6379)
        except Exception as e : 
            print("something went wrong see error below")
            logging.error(traceback.format_exc())

    def shorten_url(self, url) :
        return None