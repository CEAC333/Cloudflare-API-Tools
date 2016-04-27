import json
from sys import exit
import argparse
import requests
from config import api_token, email_address

BASE_URL = 'https://api.cloudflare.com/client/v4'

parser = argparse.ArgumentParser()
parser.add_argument('-z', '--zone', help='The top-level domain of your site.')
parser.add_argument('-c', '--cc', help='Clear all caches.')
parser.add_argument('-d', '--devmode', help='Turn development mode on or off.')
args = parser.parse_args()

# Headers that Cloudflare needs
hdrs = {
    'X-Auth-Key': api_token,
    'X-Auth-Email': email_address,
    'Content-Type': 'application/json'
}


def get_zone_id(zone, headers):
    """Return the zone ID for a give domain."""
    url = '{}/zones?name={}'.format(BASE_URL, zone)
    res = requests.request('GET', url, headers=headers)
    zid = res.json()['result'][0]['id']
    return zid


def clear_cache(zone_id, headers):
    """Clear all Cloudflare caches for a give zone ID."""
    url = '{}/zones/{}/purge_cache'.format(BASE_URL, zone_id)
    payload = '{"purge_everything": true}'
    res = requests.request('DELETE', url, headers=headers, data=payload)
    print(res.text)


def set_devmode(zone_id, headers, status='on'):
    """Sets development mode on or off."""
    url = '{}/zones/{}/settings/development_mode'.format(BASE_URL, zone_id)
    _payload = {
        'value': status.lower()
    }
    payload = json.dumps(_payload)
    res = requests.request('PATCH', url, headers=headers, data=payload)
    print(res.text)


if __name__ == '__main__':
    if args.zone:
        zid = get_zone_id(args.zone, hdrs)
    else:
        print('Please provide a zone (domain).')
        exit()

    if args.cc:
        clear_cache(zid, hdrs)

    if args.devmode:
        if args.devmode.lower() == 'on':
            set_devmode(zid, hdrs)
        elif args.devmode.lower() == 'off':
            set_devmode(zid, hdrs, status='off')
