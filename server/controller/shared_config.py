import os
from dataclasses import dataclass
try:
    from dotenv import load_dotenv
    load_dotenv()
except ModuleNotFoundError:
    pass

@dataclass(frozen=True)
class SharedConfig:
    jwt_secret: str = os.getenv('JWT_SECRET')
    jwt_algorithm: str = os.getenv('JWT_ALGORITHM')
