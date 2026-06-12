from dataclasses import dataclass

@dataclass
class Advertisement:
  model: str
  milage: int
  price: int
  link: str
  date: str
  source: str