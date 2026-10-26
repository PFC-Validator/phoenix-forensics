#!/usr/bin/env python3
"""Explicitly refresh derived upstream indexes before provenance verification."""
from generate_provenance import packet_ledger_upstream, board_upstream

packet_ledger_upstream()
board_upstream()
print('Refreshed preserved upstream indexes for the board record and packaged authority ledger.')
