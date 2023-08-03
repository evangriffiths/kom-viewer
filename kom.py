from datetime import datetime

class KOM:
    def __init__(self, post_response):
        self.segment_id: str = post_response["segment"]["id"]
        self.segment_name: str = post_response["segment"]["name"]
        self.segment_start_latitude = post_response["segment"]["start_latlng"][0]
        self.segment_start_longitude = post_response["segment"]["start_latlng"][1]
        self.datetime: datetime = datetime.strptime(
            post_response["start_date"], "%Y-%m-%dT%H:%M:%SZ"
        )

    def get_segment_url(self):
        return f"https://www.strava.com/segments/{self.segment_id}"

    def to_dict(self):
        return {
            "name": self.__str__(),
            "latitude": self.segment_start_latitude,
            "longitude": self.segment_start_longitude,
            "url": self.get_segment_url(),
            "date_string": self.datetime.strftime("%d/%m/%Y"),
        }

    def __str__(self):
        return f"{self.segment_name}"

    def __repr__(self):
        return self.__str__()