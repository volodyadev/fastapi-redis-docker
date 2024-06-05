from dataclasses import dataclass


@dataclass
class DataSchema:
    phone: str
    address: str


@dataclass
class HealthcheckSchema:
    check: str
