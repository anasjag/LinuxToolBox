from dataclasses import dataclass , field

@dataclass
class Users:
    _id: str
    fname: str 
    lname: str = None
    country_code: str = None
    phone: str = None
    email: str = None
    password: str = None
    scans: list[str] = field(default_factory=list)

@dataclass
class Scans:
    _id: str
    # user_id: Users._id
    # date: str
    # succeed: bool
    data: dict