from uuid import uuid4
from re import sub as regex_replace
from re import match as regex_match
from urllib import request
from json import loads as json_loads

from ipaddress import NetmaskValueError, AddressValueError, IPv4Network, IPv4Address, IPv6Address, IPv6Network


class FilterModule(object):
    def filters(self):
        return {
            "ensure_list": self.ensure_list,
            "safe_int_name": self.safe_int_name,
            "valid_uuid": self.valid_uuid,
            "get_uuid": self.get_uuid,
            "sanitize_name": self.sanitize_name,
            "is_valid_network": self.is_valid_network,
            "network_netmask": self.network_netmask,
            "is_dict": self.is_dict,
            "latest_recompiled_release": self.latest_recompiled_release,
        }

    @staticmethod
    def ensure_list(data: (str, list)) -> list:
        # if user supplied a string instead of a list => convert it to match our expectations
        if isinstance(data, list):
            return data

        return [data]

    @staticmethod
    def network_netmask(data: str) -> str:
        if data.find(' ') != -1:
            network = data
            address = data.split(' ', 1)[0]

        else:
            network = data
            address = data.split('/', 1)[0]

        try:
            network = IPv4Network(network)
            return f"{address} {network.netmask}"

        except (NetmaskValueError, AddressValueError):
            network = IPv6Network(network)
            return  f"{address} {network.netmask}"

    @staticmethod
    def is_valid_network(data: str) -> bool:
        network, address = None, None

        if data.find(' ') != -1:
            address = data.split(' ', 1)[0]
            network = data

        elif data.find('/') != -1:
            network = data
            address = data.split('/', 1)[0]

        if not isinstance(data, str) or data.find('/') == -1:
            return False

        try:
            IPv4Network(network)
            IPv4Address(address)
            return True

        except (NetmaskValueError, AddressValueError):
            try:
                IPv6Network(network)
                IPv6Address(address)
                return True

            except (NetmaskValueError, AddressValueError):
                return False

    @staticmethod
    def safe_int_name(key: str) -> str:
        return regex_replace('[^a-zA-Z0-9_=+.-]', '', key.replace(' ', '_'))[:15]

    @staticmethod
    def sanitize_name(name: str) -> str:
        return regex_replace('[^a-zA-Z0-9.-]', '', name.replace(' ', '_'))

    @staticmethod
    def get_uuid(_) -> str:
        return str(uuid4())

    @staticmethod
    def valid_uuid(data: str) -> bool:
        expr_uuid = r'^[a-f,0-9]{8}-[a-f,0-9]{4}-[a-f,0-9]{4}-[a-f,0-9]{4}-[a-f,0-9]{12}$'
        return regex_match(expr_uuid, data) is not None

    @staticmethod
    def is_dict(data) -> bool:
        return isinstance(data, dict)

    @staticmethod
    def _higher_version(old: str, new: str) -> bool:
        old, new = old.split('.'), new.split('.')

        try:
            return int(new[0]) > int(old[0]) or (
                    int(new[0]) == int(old[0]) and int(new[1]) > int(old[1])
            ) or (
                    int(new[0]) == int(old[0]) and int(new[1]) == int(old[1]) and int(new[2]) >
                    int(old[2])
            )

        except (IndexError, ValueError):
            return False

    @classmethod
    def latest_recompiled_release(cls, distribution: str) -> str:
        api = 'https://api.github.com/repos/ansibleguy/openvpn-recompiled/releases'
        with request.urlopen(api) as result:
            releases_ag_raw = json_loads(result.read())
        highest = '0.0.0'
        releases = {}

        for entry in releases_ag_raw:
            if cls._higher_version(old=highest, new=entry['name']):
                highest = entry['name']
                for asset in entry['assets']:
                    if asset['name'].find(distribution) != -1:
                        releases[entry['name']] = asset['browser_download_url']

        return releases[highest]
