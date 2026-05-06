#!/usr/bin/env python
"""Compile .po files to .mo files using Babel."""
import os
from babel.messages.mofile import write_mo
from babel.messages.pofile import read_po

base_dir = os.path.dirname(os.path.abspath(__file__))

for lang in ['uz', 'ru']:
    po_path = os.path.join(base_dir, 'locale', lang, 'LC_MESSAGES', 'django.po')
    mo_path = os.path.join(base_dir, 'locale', lang, 'LC_MESSAGES', 'django.mo')
    if os.path.exists(po_path):
        with open(po_path, 'r', encoding='utf-8') as f:
            catalog = read_po(f)
        with open(mo_path, 'wb') as f:
            write_mo(f, catalog)
        print(f"Compiled {po_path} to {mo_path}")
    else:
        print(f"File not found: {po_path}")
