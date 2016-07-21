#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by henri
# Copyright (c) 2016 henri
#
# License: MIT
#

"""This module exports the Luarequire plugin class."""

import re
from SublimeLinter.lint import Linter, highlight


require_re = re.compile(r"local (\w+)\s*=\s*require\s*\(([^\)]+)\)")
name_re = re.compile(r"(?:.*_)?([^_]+)")

# "          : match a "
# [^"]*?     : eat leading .s in the module name
# ([^\"\.]+) : get the module name, that contains no dots and "
# "          : end with a "
module_re = re.compile(r'"[^"]*?([^"\.]+)"')


def find_last_match(pattern, string):
    module_match = module_re.search(string)
    while module_match is not None:
        previous_match = module_match
        module_match = module_re.search(string, previous_match.end())
    return previous_match


class Luarequire(Linter):
    """Provides an interface to luarequire."""

    syntax = 'lua'
    cmd = None
    regex = re.compile(r'^(?P<line>\d+):(?P<col>\d+):(?P<message>.*)$')
    default_type = highlight.WARNING
    line_col_base = (0, 0)

    def run(self, cmd, code):

        errors = []

        for lineNumber, line in enumerate(code.split("\n")):
            match = require_re.match(line)
            if match:
                name_match = name_re.match(match.group(1))
                module_match = find_last_match(module_re, match.group(2))

                if name_match and module_match:
                    name = name_match.group(1)
                    module = module_match.group(1)
                    if name != module:
                        errors.append("{line}:{col}:{module_name} doesn't match end of variable {variable}".format(
                            line=lineNumber,
                            col=match.start(2) + module_match.start(1),
                            module_name=module,
                            variable=match.group(1)
                        ))

        return "\n".join(errors)
