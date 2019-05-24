#! /usr/bin/python3

import requests
from requests.auth import HTTPBasicAuth as hba
import json
import texttable as tt

#!/usr/bin/env python
import cherrypy
import os
import sys
import threading
import traceback
import webbrowser

from base64 import b64encode
from fitbit.api import Fitbit
from oauthlib.oauth2.rfc6749.errors import MismatchingStateError, MissingTokenError

from datetime import datetime
from datetime import timedelta

CLIENT_ID = "22D26F"
CLIENT_SECRET = "747a050f605755a65a79f2b9e0809d72"
ACCESS_TOKEN = ""
REFRESH_TOKEN = ""
FITBIT_BASE_URL = "https://api.fitbit.com/"

import pandas as pd


def getHeartRate():
    """
    心拍数を秒単位で取得する
    """
    api_ver = "1"
    detail_level = "1sec"
    # date =(datetime.now()+timedelta(days=-1)).strftime('%Y-%m-%d')
    date = "2018-12-24"
    start_time = "12:00"
    end_time = "13:00"
    url = FITBIT_BASE_URL + api_ver + "/user/-/activities/heart/date/" + \
          date + "/1d/" + detail_level + "/time/" + start_time + "/" + \
          end_time + ".json"
    headers = {"Authorization": "Bearer " + ACCESS_TOKEN}
    res = requests.get(url, headers=headers)
    jsonStr = json.loads(res.text)
    print(res.status_code)
    # 通信が行えていると200が返ってくる
    return res.text


def showTable(res_str):
    '''
    JSONをパースしてテーブル形式で出力を行う
    '''
    res_dic = json.loads(res_str)
    datas = res_dic["activities-heart-intraday"]["dataset"]
    row_list = [["TIME", "HEAT RATE"]]

    today = (datetime.now()+timedelta(days=-1)).strftime("%Y-%m-%d")

    # file = open(today+'.txt', 'w')  # 書き込みモードでオープン
    file = open('2018-12-24.txt', 'w')

    for data in datas:
        heart_rate_list = []
        heart_rate_list.append(data["time"])
        heart_rate_list.append(data["value"])
        row_list.append(heart_rate_list)
    table = tt.Texttable()
    table.set_cols_dtype(["t", "t"])
    table.set_cols_align(["l", "r"])
    table.add_rows(row_list)

    # print(table.draw())  # 表の出力
    file.writelines(table.draw())

    file.close()

class OAuth2Server:
    def __init__(self, client_id, client_secret,
                 redirect_uri='http://localhost/'):
                 #redirect_uri='http://127.0.0.1:8080/'):
        """ Initialize the FitbitOauth2Client """
        self.success_html = """
            <h1>からあげ</h1>
            <br/><h3>食べてしまったので帰れません</h3>"""
        self.failure_html = """
            <h1>ERROR: %s</h1><br/><h3>隠れた名店</h3>%s"""

        self.fitbit = Fitbit(
            # client_id,
            CLIENT_ID,
            # client_secret,
            CLIENT_SECRET,
            redirect_uri=redirect_uri,
            timeout=10,
        )

    def browser_authorize(self):
        """
        Open a browser to the authorization url and spool up a CherryPy
        server to accept the response
        """
        url, _ = self.fitbit.client.authorize_token_url()
        # Open the web browser in a new thread for command-line browser support
        threading.Timer(1, webbrowser.open, args=(url,)).start()
        cherrypy.quickstart(self)

    @cherrypy.expose
    def index(self, state, code=None, error=None):
        """
        Receive a Fitbit response containing a verification code. Use the code
        to fetch the access_token.
        """
        error = None
        if code:
            try:
                self.fitbit.client.fetch_access_token(code)
            except MissingTokenError:
                error = self._fmt_failure(
                    'Missing access token parameter.</br>Please check that '
                    'you are using the correct client_secret')
            except MismatchingStateError:
                error = self._fmt_failure('CSRF Warning! Mismatching state')
        else:
            error = self._fmt_failure('Unknown error while authenticating')
        # Use a thread to shutdown cherrypy so we can return HTML first
        self._shutdown_cherrypy()
        return error if error else self.success_html

    def _fmt_failure(self, message):
        tb = traceback.format_tb(sys.exc_info()[2])
        tb_html = '<pre>%s</pre>' % ('\n'.join(tb)) if tb else ''
        return self.failure_html % (message, tb_html)

    def _shutdown_cherrypy(self):
        """ Shutdown cherrypy in one second, if it's running """
        if cherrypy.engine.state == cherrypy.engine.states.STARTED:
            threading.Timer(1, cherrypy.engine.exit).start()



if __name__ == "__main__":

    # if not (len(sys.argv) == 3):
    #     print("Arguments: client_id and client_secret")
    #     sys.exit(1)

    # server = OAuth2Server(*sys.argv[1:])
    server = OAuth2Server("","")
    server.browser_authorize()

    profile = server.fitbit.user_profile_get()
    print('You are authorized to access data for the user: {}'.format(
        profile['user']['fullName']))

    print('TOKEN\n=====\n')
    for key, value in server.fitbit.client.session.token.items():
        print('{} = {}'.format(key, value))
        if key == "access_token":
            ACCESS_TOKEN = value
        elif key == "refresh_token":
            REFRESH_TOKEN = value

    showTable(getHeartRate())
