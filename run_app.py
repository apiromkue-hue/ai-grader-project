#!/usr/bin/env python
"""Wrapper to set up environment before running student_view."""
import sys
import os

# Add venv site-packages to path
venv_path = os.path.dirname(os.path.abspath(__file__))
site_packages = os.path.join(venv_path, 'venv', 'Lib', 'site-packages')
if site_packages not in sys.path:
    sys.path.insert(0, site_packages)

# Now run streamlit on the actual app
import streamlit.cli as st_cli

sys.argv = ['streamlit', 'run', os.path.join(venv_path, 'student_view.py')]
st_cli.main()
