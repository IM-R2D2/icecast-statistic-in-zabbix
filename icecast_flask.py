#!/usr/bin/python3

from flask import Flask, Response
import requests
import lxml.etree as ET

app = Flask(__name__)

@app.route('/listeners', methods=['GET'])
def listeners():
    # Request data of XML from Icecast
    xml_url = 'http://127.0.0.1:8000/admin/stats.xml'
    xml_response = requests.get(xml_url, auth=('adminslogin', 'passwd')) # CHANGE login/pwd from yours icecast server
    xml_data = xml_response.content

    #  Apply XSLT to XML
    xsl_path = '/usr/local/share/icecast/web/listeners_list.xsl'
    xsl_root = ET.parse(xsl_path)
    transform = ET.XSLT(xsl_root)
    xml_root = ET.XML(xml_data)
    result_tree = transform(xml_root)

    return Response(str(result_tree), content_type='text/plain')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9000)
