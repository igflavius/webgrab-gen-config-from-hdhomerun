#!/usr/bin/python3

__author__ = "Flavius Ion"
__email__ = "igflavius@odyssee.ro"
__version__ = "1.0"

import argparse
import requests
import json
import sys
from lxml import etree
from io import StringIO

def arguments():
    parser = argparse.ArgumentParser(add_help=False, description="HDHomeRun Generate Config for WebGrab++ " + __version__)
    required = parser.add_argument_group("required arguments")
    optional = parser.add_argument_group("optional arguments")
    required.add_argument("-i", "--ip", required=True, help="HDHomeRun IP Address")
    optional.add_argument("-s", "--save", default="WebGrab++.config.xml", help="Path to save config (default: WebGrab++.config.xml)")
    optional.add_argument("-h", "--help", action="help", help="Show this help message and exit")
    args = parser.parse_args()
    return args

def main():    
    try:
        req = requests.get("http://" + arg.ip + "/lineup.json").text
        data = json.loads(req)        
    except requests.RequestException:
        print("[!] unable to connect to {0}".format(arg.ip))
        sys.exit()

    # WebGrab++ Config
    xmlConfig = """    
          <settings>
          
            <filename>/storage/media/epg/guide.xml</filename>
            <postprocess grab="y" run="n">mdb</postprocess>
            <proxy>automatic</proxy>
            <user-agent>Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36</user-agent>
            <logging>on</logging>
            <retry time-out="5">4</retry>
            <skip>noskip</skip>
            <timespan>7</timespan>
            <update>f</update>

          </settings>      
          """
    
    parser = etree.XMLParser(remove_blank_text=True, ns_clean=True)
    tree = etree.parse(StringIO(xmlConfig), parser)
    root = tree.getroot()

    element = etree.Element("channels")
    for item in data:
        channel = item["GuideName"].replace(" ", "-").lower()
        channelNumber = item["GuideNumber"]
        channelName = item["GuideName"]
        subelement=etree.SubElement(element, "channel", update="i", site="cinemagia.ro", site_id=channel, xmltv_id=channelNumber)
        subelement.text = channelName
        root.append(element)
     
    with open(arg.save, "wb") as file:
        tree.write(file, encoding="utf-8", xml_declaration=True, pretty_print=True)


if __name__ == "__main__":
    arg = arguments() 
    main()