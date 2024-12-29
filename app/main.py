from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import sys
import uuid
from datetime import datetime, date
from multiprocessing import Process

from settings import configurations
from utils.log import loggerClass

import app.Constants as Constants
from app.triggers.initialMetadataLoad import runIntialCrawl

import requests
from utils.AIUtil import getMatchingRegexPattern

# Crawlee imports
from crawlee import ConcurrencySettings,Request
from crawlee.playwright_crawler import PlaywrightCrawler
from crawlee.http_clients._httpx import HttpxHttpClient
from crawlee.proxy_configuration import ProxyConfiguration

import json 

import traceback

accessTokensMap = {}
accessTokensMap['efdd18e2-4cc6-475a-b310-c9fded03a783'] = True



def create_app(env=None):
    app = Flask(__name__)
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    lg = loggerClass('generalised-crawler.log')
    lg.logger.info(env)

    Constants.env = env
    
    print(env)
    
    @app.route("/")
    def index():
        lg.logger.info('Info level log hello')
        return True
    @app.route("/ping", methods=['GET'])
    def index2():
        lg.logger.info('PING')
        return "pong", 200, {'ContentType':'application/json'}
    
    @app.route("/crawl-website", methods=['GET'])
    def crawl():
        try:
            args = request.args
            url = args.get('url')
            if(url == None or url.strip() == ""):
                return 'Incomplete req info!', 400, {'ContentType':'application/json'}
            process = Process(target=runIntialCrawl, args=(url,))
            process.start()

            
            return "Crawl started in a new thread!", 200, {'ContentType':'application/json'}
        except Exception as e:
            lg.logger.error("Issue in crawl-website API")
            lg.logger.error(e)
            lg.logger.error(traceback.format_exc())
            return 'Could not process required data!', 400, {'ContentType':'application/json'}
    
    



    
    return app
