# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

<<<<<<< HEAD
project = "DineWise"
copyright = "2024, Santhosh Reddy Mallugari, Naga Venkata Kanaka Satya Harika, Dheeraj Reddy Nalubolu"
author = (
    "Santhosh Reddy Mallugari, Naga Venkata Kanaka Satya Harika, Dheeraj Reddy Nalubolu"
)
=======
project = 'DineWise'
copyright = '2024, Santhosh Reddy Mallugari, Naga Venkata Kanaka Satya Harika, Dheeraj Reddy Nalubolu'
author = 'Santhosh Reddy Mallugari, Naga Venkata Kanaka Satya Harika, Dheeraj Reddy Nalubolu'
>>>>>>> main

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
<<<<<<< HEAD
    "sphinx.ext.autodoc",  # Automatically document from docstrings
    "sphinx.ext.viewcode",  # Add links to highlighted source code
    "sphinx.ext.napoleon",  # Support for Google-style and NumPy-style docstrings
    "sphinx.ext.intersphinx",  # Links to other documentation
    "sphinx.ext.coverage",  # Coverage checks for documentation
    "sphinx.ext.todo",  # Support for TODO notes
]

# Paths for templates
templates_path = ["_templates"]
=======
    'sphinx.ext.autodoc',  # Automatically document from docstrings
    'sphinx.ext.viewcode',  # Add links to highlighted source code
    'sphinx.ext.napoleon',  # Support for Google-style and NumPy-style docstrings
    'sphinx.ext.intersphinx',  # Links to other documentation
    'sphinx.ext.coverage',  # Coverage checks for documentation
    'sphinx.ext.todo',  # Support for TODO notes
]

# Paths for templates
templates_path = ['_templates']
>>>>>>> main

# Exclude patterns for build
exclude_patterns = []

# Ensure that Sphinx can find your project modules
import os
import sys
<<<<<<< HEAD

sys.path.insert(
    0, os.path.abspath("../")
)  # Adjust the path to point to your project's root

# -- Options for autodoc -----------------------------------------------------
autodoc_member_order = "bysource"  # Order members by source order
autodoc_default_options = {
    "members": True,  # Include class members
    "undoc-members": True,  # Include undocumented members
    "show-inheritance": True,  # Show base classes
=======
sys.path.insert(0, os.path.abspath('../'))  # Adjust the path to point to your project's root

# -- Options for autodoc -----------------------------------------------------
autodoc_member_order = 'bysource'  # Order members by source order
autodoc_default_options = {
    'members': True,  # Include class members
    'undoc-members': True,  # Include undocumented members
    'show-inheritance': True,  # Show base classes
>>>>>>> main
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

<<<<<<< HEAD
html_theme = (
    "alabaster"  # You can change this to 'sphinx_rtd_theme' for a more modern theme
)
html_static_path = ["_static"]

# Add support for linking to external documentation
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
=======
html_theme = 'alabaster'  # You can change this to 'sphinx_rtd_theme' for a more modern theme
html_static_path = ['_static']

# Add support for linking to external documentation
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
>>>>>>> main
}

# Enable TODOs in the output
todo_include_todos = True

# -- Options for Napoleon (Google/NumPy docstrings) --------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_ivar = True
napoleon_use_rtype = False
napoleon_use_param = True

# -- Additional configurations ------------------------------------------------

# Set the master document if not `index.rst`
# master_doc = 'index'
<<<<<<< HEAD
=======

>>>>>>> main
