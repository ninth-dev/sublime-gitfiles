import sys

## Reload dependencies
prefix = __package__ + "."
for module_name in [
    module_name
    for module_name in sys.modules
    if module_name.startswith(prefix) and module_name != __name__
]:
    del sys.modules[module_name]

from .commands import *
