from re import sub as regex_replace


class FilterModule(object):
    def filters(self):
        return {
            "ensure_list": self.ensure_list,
            "safe_int_name": self.safe_int_name,
        }

    @staticmethod
    def ensure_list(data: (str, list)) -> list:
        # if user supplied a string instead of a list => convert it to match our expectations
        if isinstance(data, list):
            return data

        return [data]

    @staticmethod
    def safe_int_name(key: str) -> str:
        return regex_replace('[^a-zA-Z0-9_=+.-]', '', key.replace(' ', '_'))[:15]
