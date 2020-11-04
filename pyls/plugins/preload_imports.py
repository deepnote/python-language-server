# Copyright 2017 Palantir Technologies, Inc.
import logging
from pyls import hookimpl

log = logging.getLogger(__name__)

MODULES = [
    "numpy", "tensorflow", "sklearn", "array", "binascii", "cmath", "collections",
    "datetime", "errno", "exceptions", "gc", "imageop", "imp", "itertools",
    "marshal", "math", "matplotlib", "mmap", "mpmath", "msvcrt", "networkx", "nose", "nt",
    "operator", "os", "os.path", "pandas", "parser", "scipy", "signal",
    "skimage", "statsmodels", "strop", "sympy", "sys", "thread", "time", "wx", "zlib"
]


@hookimpl
def pyls_settings():
    # Setup default modules to preload, and rope extension modules
    return {
        'plugins': {'preload': {'modules': MODULES}},
        'rope': {'extensionModules': MODULES}
    }


@hookimpl
def pyls_initialize(config):
    for mod_name in config.plugin_settings('preload').get('modules', []):
        try:
            __import__(mod_name)
            log.debug("Preloaded module %s", mod_name)
        except Exception:  # pylint: disable=broad-except
            # Catch any exception since not only ImportError can be raised here
            # For example, old versions of NumPy can cause a ValueError.
            # See spyder-ide/spyder#13985
            pass
