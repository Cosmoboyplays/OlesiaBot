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
        users = self.get_users()
        users.append(user_id)
        self._write({"users": users, "started": True})

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
        self._write({"started": False, 'users': []})


