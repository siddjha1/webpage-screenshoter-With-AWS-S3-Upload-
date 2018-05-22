from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import boto3
from botocore.client import Config
from boto.cloudfront import CloudFrontConnection
import os
import time


class Screenshooter():
    def __init__(self,chunksize=1):
        self.KEY_ID = 'ENTER AWS KEY'
        self.ACCESS_KEY = 'ENTER AWS ACCESS KEY'
        self.bucket = 'ENTER S3 BUCKET NAME'
        self.conn=None
        self.s3=None
        self.sku=None
        self.driver=None
        self.counter = chunksize
        self.n = 0;

    def connect(self):
        print('Connecting to S3')
        self.s3 = boto3.resource('s3', aws_access_key_id=self.KEY_ID, aws_secret_access_key=self.ACCESS_KEY,config=Config(signature_version='s3v4'))
        
    def uploadFilesToS3(self, path, keyPath):
        path = path.replace('\\', '/')
        if os.path.isfile(path):
            key = keyPath
            bucket = self.bucket
            try:
                data = open(path, 'rb')
                self.s3.Bucket(bucket).put_object(Key=key, Body=data)
                print('Uploading '+path+' to Amazon S3 bucket')
            except:
                print('failed upload')

    def open_browser(self):
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
        self.driver = webdriver.Firefox(firefox_profile=firefox_profile)

    def get_thumbnails(self, url, height=1024, width=768):
        print('Navigating to '+url)
        try:
            self.driver.get(url)
        except:
            print("Unable to navigate to "+url)
        self.driver.set_window_size(height, width)

        time.sleep(5)  # delays for 5 seconds. You can Also Use Float Value.
        self.driver.save_screenshot('Thumbnails/Thumbail.png')

Screenshooter = Screenshooter()
Screenshooter.connect()
Screenshooter.open_browser()
Screenshooter.get_thumbnails('http://www.google.com',1024,768)
Screenshooter.driver.quit()
