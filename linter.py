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
module_re = re.compile(r'"(\w+?)"')


class Luarequire(Linter):
    """Provides an interface to luarequire."""

    syntax = 'lua'
    cmd = None
    regex = re.compile(r'^(?P<line>\d+):(?P<col>\d+):(?P<message>.*)$')
    default_type = highlight.WARNING

    def run(self, cmd, code):

        errors = []

        for lineNumber, line in enumerate(code.split("\n")):
            match = require_re.match(line)
            if match:
                name_match = name_re.match(match.group(1))
                modules_results = module_re.findall(match.group(2))
                if name_match and modules_results:
                    name = name_match.group(1)
                    module = modules_results[-1]
                    if name != module:
                        errors.append("{line}:{col}:{module_name} doesn't match end of variable {variable}".format(
                            line=lineNumber + 1,
                            col=line.find('"{}"'.format(module)) + 2,
                            module_name=module,
                            variable=match.group(1)
                        ))

        return "\n".join(errors)
