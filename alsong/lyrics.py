from urllib import request
import xml.etree.ElementTree as ET


def GetLyricList(title, artist=""):
    if title == "" and artist == "":
        return []
    body = """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope
	xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope"
	xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xmlns:xsd="http://www.w3.org/2001/XMLSchema"
	xmlns:ns2="ALSongWebServer/Service1Soap"
	xmlns:ns1="ALSongWebServer"
	xmlns:ns3="ALSongWebServer/Service1Soap12">
	<SOAP-ENV:Body>
		<ns1:GetResembleLyricList2>
			<ns1:encData>7c2d15b8f51ac2f3b2a37d7a445c3158455defb8a58d621eb77a3ff8ae4921318e49cefe24e515f79892a4c29c9a3e204358698c1cfe79c151c04f9561e945096ccd1d1c0a8d8f265a2f3fa7995939b21d8f663b246bbc433c7589da7e68047524b80e16f9671b6ea0faaf9d6cde1b7dbcf1b89aa8a1d67a8bbc566664342e12</ns1:encData>
			<ns1:title>{}</ns1:title>
			<ns1:artist>{}</ns1:artist>
			<ns1:pageNo>1</ns1:pageNo>
		</ns1:GetResembleLyricList2>
	</SOAP-ENV:Body>
</SOAP-ENV:Envelope>"""
    dataStr = body.format(title, artist)
    header = {
        "Content-Type": "application/soap+xml; charset=utf-8",
        "User-Agent": "gSOAP/2.7",
        "Host": "lyrics.alsong.co.kr",
    }
    data = dataStr.encode("UTF-8")
    req = request.Request(
        "http://lyrics.alsong.co.kr/alsongwebservice/service1.asmx",
        data=data,
        headers=header,
    )
    res = request.urlopen(req)

    ns = {
        "soap": "http://www.w3.org/2003/05/soap-envelope",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xsd": "http://www.w3.org/2001/XMLSchema",
        "": "ALSongWebServer",
    }

    lyrics_list = ET.fromstring(res.read()).findall(
        "soap:Body/GetResembleLyricList2Response/GetResembleLyricList2Result/ST_SEARCHLYRIC_LIST",
        ns,
    )

    songs = []
    for lyric_tag in lyrics_list:
        temp = {}
        temp["lyricId"] = lyric_tag.find("lyricID", ns).text
        temp["title"] = (
            lyric_tag.find("title", ns).text.replace("&lt;", "<").replace("&gt;", ">")
        )
        temp["artist"] = (
            lyric_tag.find("artist", ns).text.replace("&lt;", "<").replace("&gt;", ">")
        )
        temp["album"] = (
            lyric_tag.find("album", ns).text.replace("&lt;", "<").replace("&gt;", ">")
        )
        songs.append(temp)
    return songs


def GetLyric(Id):
    body = """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope
	xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope"
	xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xmlns:xsd="http://www.w3.org/2001/XMLSchema"
	xmlns:ns2="ALSongWebServer/Service1Soap"
	xmlns:ns1="ALSongWebServer"
	xmlns:ns3="ALSongWebServer/Service1Soap12">
	<SOAP-ENV:Body>
		<ns1:GetLyricByID2>
			<ns1:encData>7c2d15b8f51ac2f3b2a37d7a445c3158455defb8a58d621eb77a3ff8ae4921318e49cefe24e515f79892a4c29c9a3e204358698c1cfe79c151c04f9561e945096ccd1d1c0a8d8f265a2f3fa7995939b21d8f663b246bbc433c7589da7e68047524b80e16f9671b6ea0faaf9d6cde1b7dbcf1b89aa8a1d67a8bbc566664342e12</ns1:encData>
			<ns1:lyricID>{}</ns1:lyricID>
		</ns1:GetLyricByID2>
	</SOAP-ENV:Body>
</SOAP-ENV:Envelope>"""

    dataStr = body.format(str(Id))
    header = {
        "Content-Type": "application/soap+xml; charset=utf-8",
        "User-Agent": "gSOAP/2.7",
        "Host": "lyrics.alsong.co.kr",
    }
    data = dataStr.encode("UTF-8")
    req = request.Request(
        "http://lyrics.alsong.co.kr/alsongwebservice/service1.asmx",
        data=data,
        headers=header,
    )
    res = request.urlopen(req)

    ns = {
        "soap": "http://www.w3.org/2003/05/soap-envelope",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xsd": "http://www.w3.org/2001/XMLSchema",
        "": "ALSongWebServer",
    }

    result = ET.fromstring(res.read()).find("soap:Body/GetLyricByID2Response", ns)

    if result.find("GetLyricByID2Result", ns).text != "true":
        return None
    else:
        return result.find("output/lyric", ns).text