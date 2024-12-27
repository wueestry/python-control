# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../'))

# Use the readthedocs.org theme if installed
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if not on_rtd:  # only import and set the theme if we're building docs locally
    try:
        import sphinx_rtd_theme
        html_theme = 'sphinx_rtd_theme'
    except ImportError:
        html_theme = 'default'

# -- Project information -----------------------------------------------------

project = u'Python Control Systems Library'
copyright = u'2023, python-control.org'
author = u'Python Control Developers'

# Version information - read from the source code
import re
import control

# Get the version number for this commmit (including alpha/beta/rc tags)
release = re.sub('^v', '', os.popen('git describe').read().strip())

# The short X.Y.Z version
version = re.sub(r'(\d+\.\d+\.\d+(.post\d+)?)(.*)', r'\1', release)

print("version %s, release %s" % (version, release))

# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
needs_sphinx = '3.4'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc', 'sphinx.ext.todo', 'sphinx.ext.intersphinx',
    'sphinx.ext.imgmath', 'sphinx.ext.autosummary', 'nbsphinx', 'numpydoc',
    'sphinx.ext.linkcode', 'sphinx.ext.doctest', 'sphinx_copybutton'
]

# scan documents for autosummary directives and generate stub pages for each.
autosummary_generate = True

# list of autodoc directive flags that should be automatically applied
# to all autodoc directives.
autodoc_default_options = {
    'members': True,
    'inherited-members': True,
    'exclude-members': '__init__, __weakref__, __repr__, __str__'
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = [u'_build', 'Thumbs.db', '.DS_Store',
                    '*.ipynb_checkpoints']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# This config value contains the locations and names of other projects that
# should be linked to in this documentation.
intersphinx_mapping = \
    {'scipy': ('https://docs.scipy.org/doc/scipy', None),
     'numpy': ('https://numpy.org/doc/stable', None),
     'matplotlib': ('https://matplotlib.org/stable/', None),
     }

# If this is True, todo and todolist produce output, else they produce nothing.
# The default is False.
todo_include_todos = True


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".

html_static_path = ['_static']
def setup(app):
    app.add_css_file('css/custom.css')

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}

# -----------------------------------------------------------------------------
# Source code links (from numpy)
# -----------------------------------------------------------------------------

import inspect
from os.path import relpath, dirname

def linkcode_resolve(domain, info):
    """
    Determine the URL corresponding to Python object
    """
    if domain != 'py':
        return None

    modname = info['module']
    fullname = info['fullname']

    submod = sys.modules.get(modname)
    if submod is None:
        return None

    obj = submod
    for part in fullname.split('.'):
        try:
            obj = getattr(obj, part)
        except Exception:
            return None

    # strip decorators, which would resolve to the source of the decorator
    # possibly an upstream bug in getsourcefile, bpo-1764286
    try:
        unwrap = inspect.unwrap
    except AttributeError:
        pass
    else:
        obj = unwrap(obj)

    # Get the filename for the function
    try:
        fn = inspect.getsourcefile(obj)
    except Exception:
        fn = None
    if not fn:
        return None

    # Ignore re-exports as their source files are not within the numpy repo
    module = inspect.getmodule(obj)
    if module is not None and not module.__name__.startswith("control"):
        return None

    try:
        source, lineno = inspect.getsourcelines(obj)
    except Exception:
        lineno = None

    fn = relpath(fn, start=dirname(control.__file__))

    if lineno:
        linespec = "#L%d-L%d" % (lineno, lineno + len(source) - 1)
    else:
        linespec = ""

    base_url = "https://github.com/python-control/python-control/blob/"
    if release != version:      # development release
        return base_url + "main/control/%s%s" % (fn, linespec)
    else:                       # specific version
        return base_url + "%s/control/%s%s" % (version, fn, linespec)

# Don't automaticall show all members of class in Methods & Attributes section
numpydoc_show_class_members = False

# Don't create a Sphinx TOC for the lists of class methods and attributes
numpydoc_class_members_toctree = False

# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'PythonControlLibrarydoc'


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'python-control.tex',
     u'Python Control Systems Library User Guide',
     u'Python Control Developers', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'pythoncontrollibrary', u'Python Control Library Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'PythonControlLibrary', u'Python Control Library Documentation',
     author, 'PythonControlLibrary', 'One line description of project.',
     'Miscellaneous'),
]

# -- Options for doctest ----------------------------------------------

# Import control as ct
doctest_global_setup = """
import numpy as np
import control as ct
import control.optimal as obc
import control.flatsys as fs
import control.phaseplot as pp
ct.reset_defaults()
"""
