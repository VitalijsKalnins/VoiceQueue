from app.enum.profiles import ProfileEntityType

class ProfileEntity:
    def __init__(
        self,
        text: str = "",
        type: ProfileEntityType = ProfileEntityType.UNKNOWN,
        sentiment: float = 0.0,
    ):
        self.text = text
        self.type = type
        self.sentiment = sentiment