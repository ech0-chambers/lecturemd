
from enum import Enum
import platform

class Platform(Enum):
    LINUX = 0
    WINDOWS = 1
    MAC = 2
    JAVA = 3
    UNKNOWN = 4


def get_platform() -> Platform:
    """Get the current platform.

    Returns
    -------
    Platform
        The current platform.
    """    
    system = platform.system()
    if system == "Linux":
        return Platform.LINUX
    elif system == "Windows":
        return Platform.WINDOWS
    elif system == "Darwin":
        return Platform.MAC
    elif system == "Java":
        return Platform.JAVA
    else:
        return Platform.UNKNOWN