import sys
import http
import http.cookiejar
import json
from urllib.parse import quote

m_host = "rink.hockeyapp.net"
KoAAndriodToken = "*****"
KoAIOSToken = "****"
Infoheader = {"Host": m_host,
              "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.1.20) Gecko/20081217 (FoxPlus) Firefox/2.0.0.20",
              "Content-Type": "application/x-www-form-urlencoded",
              "X-HockeyAppToken": KoAIOSToken}

baseurl = "/api/2/apps/"

# 连接服务器
conn = http.client.HTTPSConnection(m_host)
conn.connect()

def GetAppID():
    conn.request("GET", baseurl, None, Infoheader)
    appinfostr = conn.getresponse().read().decode("utf-8")
    print(appinfostr)
    appinfoobj = json.loads(appinfostr)
    return appinfoobj["apps"][0]["public_identifier"]

def GetAppVersionID(appid, shortversion, version):
    appversionurl = baseurl + appid + "/app_versions"
    conn.request("GET", appversionurl, None, Infoheader)
    appversioninfostr = conn.getresponse().read().decode("utf-8")
    print(appversioninfostr)
    appversioninfoobj = json.loads(appversioninfostr)
    for versioninfo in appversioninfoobj["app_versions"]:
        if versioninfo["version"] == version and versioninfo["shortversion"] == shortversion:
            return versioninfo["id"]

def GetUrlResponse(url):
    conn.request("GET", url, None, Infoheader)
    return conn.getresponse().read().decode("utf-8")

def GetSpecificCrashGroup(appid, appversion, page, querycondition):
    crashgroupinfourl = baseurl + appid + "/app_versions/" + str(
        appversion) + "/crash_reasons/search?page=" + str(page) + "&per_page=100"
    searchurl = '&query=' + quote(querycondition)
    print(crashgroupinfourl + searchurl)
    return GetUrlResponse(crashgroupinfourl + searchurl)

def GetSpecificCrashes(appid, appversion, page, querycondition):
    crashgroupinfourl = baseurl + appid + "/app_versions/" + str(
        appversion) + "/crashes/search?page=" + str(page) + "&per_page=100"
    searchurl = '&query=' + quote(querycondition) + "&type=crashes"
    print(crashgroupinfourl + searchurl)
    return GetUrlResponse(crashgroupinfourl + searchurl)

def GetSpecificCrash(appid, reasonid, page):
    crashesinfourl = baseurl + appid + "/crash_reasons/" + str(reasonid) + "?page=" + str(page) + "&per_page=100"
    print(crashesinfourl)
    return GetUrlResponse(crashesinfourl)

def GetSpecificCrashLog(appid, crashid):
    crashesinfourl = baseurl + appid + "/crashes/" + str(crashid) + "?format=log"
    print(crashesinfourl)
    return GetUrlResponse(crashesinfourl)

def GetCrashGroup(appid, appversion, page):
    crashgroupinfourl = baseurl + appid + "/app_versions/" + str(
        appversion) + "/crash_reasons.html?page=" + str(page) + "&per_page=100&sort=number_of_crashes&order=desc"
    print(crashgroupinfourl)
    return GetUrlResponse(crashgroupinfourl)

def GetUTCDate(timestr):
    words = timestr.split()
    # for word in words:
    #     print(word)
    day = int(words[3])
    hourinday = words[4][0:2]
    timezone = words[5]
    sign = timezone[3]
    offset = timezone[4:6]
    # print("time in day " + sign + " " + offset)
    if '+' == sign and hourinday < offset:
        return day - 1
    elif '-' == sign and hourinday + offset >= '24':
        return day + 1
    else:
        return day - 1

