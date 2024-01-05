from dataclasses import dataclass , field
from typing import List
@dataclass
class Users:
    _id: str
    fname: str 
    lname: str = None
    country_code: str = None
    phone: str = None
    email: str = None
    password: str = None
    scans: List[str] = field(default_factory=list)

@dataclass
class Scans:
    _id: str
    date: str
    status: str
    ip: str
    data: dict
    tool_name: str

@dataclass
class Pings:
    _id: str
    data: str
    status: str
    ip: str
    date: str
    tool_name: str