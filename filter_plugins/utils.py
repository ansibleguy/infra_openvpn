from uuid import uuid4
from re import sub as regex_replace
from re import match as regex_match

from ipaddress import NetmaskValueError, AddressValueError, IPv4Network, IPv4Address, IPv6Address, IPv6Network


class FilterModule(object):
    def filters(self):
        return {
            "ensure_list": self.ensure_list,
            "safe_int_name": self.safe_int_name,
            "valid_uuid": self.valid_uuid,
            "get_uuid": self.get_uuid,
            "sanitize_name": self.sanitize_name,
            "is_ipaddress_cidr": self.is_ipaddress_cidr,
        }

    @staticmethod
    def ensure_list(data: (str, list)) -> list:
        # if user supplied a string instead of a list => convert it to match our expectations
        if isinstance(data, list):
            return data

        return [data]

    @staticmethod
    def is_ipaddress_cidr(data: str) -> bool:
        network = data
        address = data.split('/', 1)[0]

        if not isinstance(data, str) or data.find('/') == -1:
            return False

        try:
            IPv4Network(network, strict=False)
            IPv4Address(address)
            return True

        except (NetmaskValueError, AddressValueError):
            try:
                IPv6Network(network, strict=False)
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
