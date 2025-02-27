from wherev2 import findipadlist
import http.client
import json
import argparse
import textfsm
# API Documentation https://ip-api.com/docs

fieldslist = ['status', 'message', 'country', 'countryCode',
              'region', 'regionName', 'city', 'isp', 'org', 'as', 'query']
fields = ",".join(fieldslist)
# fields = '66842623'


headers={'Content-Type': 'application/json','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'}


import http.client
import urllib.parse
from getpass import getpass
import os
import base64  # Import base64 for proxy authentication

def make_proxy_request(url, method="GET", headers=None, body=None, proxy_host=None, proxy_port=None, proxy_user=None, proxy_pass=None):
    """
    Makes an HTTP request through a proxy.

    Args:
        url: The URL to request.
        method: The HTTP method (GET, POST, PUT, DELETE, etc.). Defaults to GET.
        headers: A dictionary of headers to send with the request. Defaults to None.
        body: The body of the request (for POST, PUT, etc.). Defaults to None.
        proxy_host: The hostname or IP address of the proxy server.
        proxy_port: The port of the proxy server.
        proxy_user: Username for proxy authentication (optional).
        proxy_pass: Password for proxy authentication (optional).

    Returns:
        Json Object.  
        Raises exceptions for connection errors or invalid responses.
    """
    try:
        parsed_url = urllib.parse.urlparse(url)
        scheme = parsed_url.scheme
        hostname = parsed_url.netloc
        path = parsed_url.path or "/"  # Handle cases where path is empty
        if parsed_url.query:
            path += "?" + parsed_url.query


        if proxy_host and proxy_port:
            # Using a proxy
            if scheme == "https":
                conn = http.client.HTTPSConnection(proxy_host, proxy_port)
                # Important: You must tunnel HTTPS through the proxy using CONNECT
                conn.set_tunnel(hostname, 443)  # Tunnel to the actual host
            else:
                conn = http.client.HTTPConnection(proxy_host, proxy_port)


            if proxy_user and proxy_pass:
                # Add proxy authentication header
                if headers is None:
                    headers = {}
                auth_string = f"{proxy_user}:{proxy_pass}".encode("utf-8")
                base64_auth = base64.b64encode(auth_string).decode("utf-8")
                headers["Proxy-Authorization"] = f"Basic {base64_auth}"

            # Important: Send the full URL to the proxy (except for HTTPS CONNECT)
            if scheme != "https":
                conn.request(method, url, body=body, headers=headers) # Full URL for HTTP
            else:
              conn.request(method, path, body=body, headers=headers) # Path only for HTTPS CONNECT


        else:
            # No proxy
            if scheme == "https":
                conn = http.client.HTTPSConnection(hostname)
            else:
                conn = http.client.HTTPConnection(hostname)
            conn.request(method, path, body=body, headers=headers)

        response = conn.getresponse()
        status_code = response.status
        response_body = response.read()
        conn.close()
        return json.loads(response_body.decode('utf-8'))
    except Exception as e:
        print(f"Error fetching IP details: {e}")
        return None


def get_multiline_input():
    print("Enter multiple lines of text. Type 'END' when finished.")

    input_lines = []
    while True:
        line = input()
        if line.strip().upper() == 'END':
            break
        input_lines.append(line)

    return "\n".join(input_lines)


def parse_text_with_textfsm(input_text, template_path):
    data = []
    try:
        with open(template_path, 'r') as template_file:
            template = textfsm.TextFSM(template_file)
        parsed_data = template.ParseText(input_text)
        # print(template.header)
        for row in parsed_data:
            data.append(dict(zip(template.header, row)))
        return (data)
        # return parsed_data, template.header
    except FileNotFoundError:
        print(f"Error: Template file '{template_path}' not found.")
        return data
    except textfsm.TextFSMError as e:
        print(f"Error parsing text with TextFSM: {e}")
        return data


def formatlistdictbykeys(primarykey='query', inputlist=[]):
    """
    converts lists dict to dictionary with values as list by the specified key

    Args:
      set as primary key of the list

    Returns:
      a dictionary with key
    """
    data = {}
    for x in inputlist:
        data[x[primarykey]] = x
    return data


if __name__ == "__main__":
    # Argparse setup
    parser = argparse.ArgumentParser(
        description="Get location information for an IP address.")
    parser.add_argument("ip_address", nargs="?",
                        help="The IP address to look up.", default="")
    parser.add_argument("-m", "--multiline",  default=False,
                        help="multiline input to look up", action='store_true')
    parser.add_argument("-f", "--fulldetail",  default=False,
                        help="show full details, only available for single input", action='store_true')
    args = parser.parse_args()
    ip_address = args.ip_address
    print(f'use -h option for help')
    urlmain = "http://ip-api.com"
    proxy_host = "10.97.216.133"  # Replace with your proxy host
    proxy_port = 8080  # Replace with your proxy port
    print(f'password required for webproxy server:{proxy_host}:{proxy_port}')
    proxy_user = os.getenv('USERNAME')
    proxy_pass = getpass(f'{proxy_user}@password:')
    
    if (args.multiline):
        inputlines = get_multiline_input()
        # print(inputlines)
        # print('*'*10)
        outputdict = parse_text_with_textfsm(
            inputlines, 'findipaddress.textfsm')

        listofips = []
        for x in outputdict:
            listofips += list(x.values())
        # remove duplicates
        listofips = list(dict.fromkeys(listofips))
        # locationdatareturn =[]
        url = f'{urlmain}/batch?fields={fields}'
        locationdatareturn = make_proxy_request(url, method="POST", headers=None, body=json.dumps(listofips), proxy_host=proxy_host, proxy_port=proxy_port, proxy_user=proxy_user, proxy_pass=proxy_pass)
        #locationdatareturn = get_ip_locations(apifunction=f'/batch?{fields}', payload=json.dumps(listofips))
        keyips = formatlistdictbykeys(inputlist=locationdatareturn)
        print(f'{"*"*10}output{"*"*10}')
        for line in inputlines.splitlines():
            ipmatch = ''
            for keyip in keyips.keys():
                if keyip in line:
                    # ipmatch = f'ip:{keyips[keyip]["query"]},as:{keyips[keyip]["as"]},country:{keyips[keyip]["countryCode"]},region:{keyips[keyip]["region"]},isp:{keyips[keyip]["isp"]}'
                    ipmatch = f'ip:{keyips[keyip].get("query")},as:{keyips[keyip].get("as")},country:{keyips[keyip].get("countryCode")},region:{keyips[keyip].get("region")},isp:{keyips[keyip].get("isp")}'
                    ipmatchwhere = []
                    ipmatchwhere = findipadlist(findaddr=keyip)
                    if ipmatchwhere:
                        localmatchedhost = ipmatchwhere[0].split(',')[0]
                        ipmatch = f'as:{keyips[keyip].get("as")},host:{localmatchedhost}'
            if ipmatch:
                print(f'{line} -> {ipmatch}')
            else:
                print(f'{line}')

    elif (ip_address):
        #location_data = get_ip_location_http_client(ip_address)
        url = f'{urlmain}/json/{ip_address}?fields={fields}'
        location_data = make_proxy_request(url, method="GET", headers=None, body=None, proxy_host=proxy_host, proxy_port=proxy_port, proxy_user=proxy_user, proxy_pass=proxy_pass)
        if location_data:
            if args.fulldetail:
                for k, v in location_data.items():
                    print(f'{k}:{v}')
            else:
                print(
                    f'ip:{location_data.get("query")},as:{location_data.get("as")},country:{location_data.get("countryCode")},region:{location_data.get("region")},isp:{location_data.get("isp")}')
            #
            # Print other location details as needed
        else:
            print(f"Failed to retrieve location information for {ip_address}")
    else:
        print(f"IP Address not provided")
