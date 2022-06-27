import logging

try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:   # for Python < 3.8
    from importlib_metadata import version, PackageNotFoundError


try:
    __version__ = version(__name__)
except PackageNotFoundError:
    # package is not installed
    pass

logging.getLogger(__name__).addHandler(logging.NullHandler())


__all__ = ['create_database',
           'generate_SNRs_FARs',
           'gibbs_sample',
           'p_astro_utils',
           'select_hyperposterior',
           ]