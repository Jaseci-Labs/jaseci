"""Subnode Table building pass.

This pass builds a table of subnodes for each node in the AST. This is used
for fast lookup of nodes of a certain type in the AST. This is just a utility
pass and is not required for any other pass to work.
"""
