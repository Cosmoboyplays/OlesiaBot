import json


class NewsletterManager:
    """
    JSON exmaple
    ------
    {
        "users": [1, 2, 3],
        "started": true/false
    }
    """
    def __init__(self, filename: str = "newsletter.json") -> None:
        self.filename = filename

    def _read(self) -> dict:
        with open(self.filename) as f:
            return json.load(f)

    def _write(self, date: dict) -> None:
        with open(self.filename, "w") as f:
            json.dump(date, f)

    def add_user(self, user_id: int) -> None:
        """
        Add user to list
        :param user_id:
        :return: 
        """
        d = self._read()
        d["users"].append(user_id)
        self._write(d)

    def get_users(self) -> list[int]:
        """
        Get list of users
        :return: 
        """
        return self._read()["users"]

    def is_started(self):
        """
        Check if newsletter is started
        :return: 
        """
        return self._read()["started"]

    def start(self) -> None:
        """
        Start newsletter
        :return: 
        """
        d = self._read()
        d["started"] = True
        self._write(d)

    def stop(self) -> None:
        """
        Stop newsletter
        :return: 
        """
        d = self._read()
        d["started"] = True
        d["users"] = []
        self._write(d)

    def get_list_name(self) -> str:
        return self._read()['list_name']

    def update_list_name(self, list_name: str) -> None:
        data = self._read()
        data["list_name"] = list_name
        self._write(data)



