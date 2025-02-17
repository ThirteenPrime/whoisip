import http.client
import json
import argparse
import textfsm
# API Documentation https://ip-api.com/docs

fieldslist = ['status', 'message', 'country', 'countryCode',
              'region', 'regionName', 'city', 'isp', 'org', 'as', 'query']
fields = ",".join(fieldslist)
#fields = '66842623'


def get_ip_location_http_client(ip_address):
    """
    Fetches location information for a given IP address using the ip-api.com service.

    Args:
      ip_address: The IP address to look up.

    Returns:
      A dictionary containing location information (city, region, country, etc.) 
      if the request is successful, otherwise None.
    """
    try:
        # context = ssl._create_unverified_context()
        conn = http.client.HTTPConnection("ip-api.com", timeout=4)
        # fields = "60959"

        conn.request("GET", f"/json/{ip_address}?fields={fields}")
        resp = conn.getresponse()
        data = resp.read()
        conn.close()
        return json.loads(data.decode('utf-8'))
    except Exception as e:
        print(f"Error fetching IP details: {e}")
        return None


def get_ip_locations(method='POST', apifunction='/batch?fields=7401471', payload="", headers={'Content-Type': 'application/json'}):
    """
    Fetches location information for a list of IP addresses using the ip-api.com batch endpoint.

    Args:
      ips: A list of IP addresses to look up.

    Returns:
      A list of dictionaries, each containing location information for an IP address.
    """
    try:
        conn = http.client.HTTPConnection("ip-api.com", timeout=4)
        conn.request(method, apifunction, payload, headers)
        resp = conn.getresponse()
        if resp.status != 200:
            print(f"HTTP Error: {resp.status} {resp.reason}")
            return None
        data = resp.read().decode('utf-8')
        conn.close()
        return json.loads(data)
    except Exception as e:
        print(f"Error fetching IP locations: {e}")
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
    if (args.multiline):
        inputlines = get_multiline_input()
        outputdict = parse_text_with_textfsm(
            inputlines, 'findipaddress.textfsm')
        # print(outputdict)
        listofips = []
        for x in outputdict:
            listofips += list(x.values())
        # remove duplicates
        listofips = list(dict.fromkeys(listofips))
        # locationdatareturn =[]
        locationdatareturn = get_ip_locations(
            apifunction=f'/batch?{fields}', payload=json.dumps(listofips))
        keyips = formatlistdictbykeys(inputlist=locationdatareturn)
        for line in inputlines.splitlines():
            ipmatch = ''
            for keyip in keyips.keys():
                if keyip in line:
                    # ipmatch = f'ip:{keyips[keyip]["query"]},as:{keyips[keyip]["as"]},country:{keyips[keyip]["countryCode"]},region:{keyips[keyip]["region"]},isp:{keyips[keyip]["isp"]}'
                    ipmatch = f'ip:{keyips[keyip].get("query")},as:{keyips[keyip].get("as")},country:{keyips[keyip].get("countryCode")},region:{keyips[keyip].get("region")},isp:{keyips[keyip].get("isp")}'
            if ipmatch:
                print(f'{line} -> {ipmatch}')
            else:
                print(f'{line}')

    elif (ip_address):
        location_data = get_ip_location_http_client(ip_address)
        if location_data:
            if args.fulldetail:
                for k, v in location_data.items():
                    print(f'{k}:{v}')
            else:
                print(
                    f'ip:{location_data["query"]},as:{location_data["as"]},country:{location_data["countryCode"]},region:{location_data["region"]},isp:{location_data["isp"]}')
            #
            # Print other location details as needed
        else:
            print(f"Failed to retrieve location information for {ip_address}")
    else:
        print(f"IP Address not provided")
