import json
import http.client
import ssl


def get_ip_location_http_client():
    """
    Fetches location information for a given IP address using the ip-api.com service.

    Args:
      ip_address: The IP address to look up.

    Returns:
      A dictionary containing location information (city, region, country, etc.) 
      if the request is successful, otherwise None.
    """
    try:
        context = ssl._create_unverified_context()
        conn = http.client.HTTPSConnection(
            "rwhois.he.net", timeout=4)
        # fields = "60959"

        conn.request(
            method="GET", url=f"/whois.php?query=103.200.13.243")
        # conn.request(method, apifunction, payload, headers)
        resp = conn.getresponse()
        data = resp.read()
        conn.close()
        # return json.loads(data.decode('utf-8'))
        return data
    except Exception as e:
        print(f"Error fetching IP details: {e}")
        return None


print(get_ip_location_http_client())
