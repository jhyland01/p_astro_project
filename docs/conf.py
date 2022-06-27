# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'P_astro Project'
copyright = '2022, Johnathon Hyland'
author = 'Johnathon Hyland'

release = '0.1'
version = '0.1.0'

import os
import sys


import P_astro_project

sys.path.insert(0, os.path.abspath("../"))

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    "sphinx.ext.autodoc",
    "sphinx.ext.mathjax",
    'sphinx.ext.doctest',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    "sphinx.ext.viewcode",
]
autosummary_generate = True

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# The master toctree document.
master_doc = "index"

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'

# -- Configure autoapi -------------------------------------------------------
autoapi_type = 'python'
autoapi_dirs = ['../analysis/']
autoapi_add_toctree_entry = False
autoapi_options = ['members', 'show-inheritance',
                   'show-module-summary']