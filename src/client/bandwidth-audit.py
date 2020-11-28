#!/usr/bin/env python

import configparser
import speedtest
import sys, os
from datetime import date
import random
from time import sleep
import http.client
import json
import sys

# Variable Scope
config = configparser.ConfigParser()
config.read (os.path.dirname(os.path.abspath(__file__)) + '/bandwidth-audit.cfg')
max_dl_mbps = config['DEFAULT']['contracted_bandwidth_mbps_download']
max_up_mbps = config['DEFAULT']['contracted_bandwidth_mbps_upload']
authtoken = config ['DEFAULT']['token']


def runTest():
    servers = []
    threads = None
    #User information
    s = speedtest.Speedtest()
    ISP =  s.config['client']['isp']
    ip = s.config['client']['ip']
    country = s.config['client']['country']
    #Get server list
    s.get_servers(servers)

    sponsorinfo = s.get_best_server()
    sponsor = sponsorinfo['sponsor']
    sponsorID = sponsorinfo['id']
    sponsorCC = sponsorinfo['cc']
    dlbits = s.download(threads=threads) / 1000.0 / 1000.0
    dlmbps = '%0.2f' % dlbits
    upbits = s.upload(threads=threads) / 1000.0 / 1000.0
    upmbps = '%0.2f' % upbits
    latency = s.results.server['latency']
    resultsurl = s.results.share()
    dic_results = {"UserToken": authtoken , "ContractedUpload": max_up_mbps , "ContractedDownload": max_dl_mbps, "ISP" : ISP ,"Country" : country ,"Sponsor": sponsor, "SponsorID": sponsorID,"SponsorCC":sponsorCC,"Latency":latency,"DlMbps":dlmbps,"Upmbps":upmbps,"ResultImage":resultsurl}
    json_object = json.dumps(dic_results)
    return (json_object)
    


def main():
    while True:
        minutes = random.randint(120 , 1440 )
        print ("Next sample in ",minutes)
        sleep (minutes * 60)
        summitSample()

def summitSample():
    sampleResults = runTest()
    conn = http.client.HTTPSConnection('theip.xyz/bandwidth-audit-getsample')
    print (sampleResults)
    conn.request("POST", '/', sampleResults, {'Content-Type': 'application/json',})
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

if __name__ == "__main__":
    main()



