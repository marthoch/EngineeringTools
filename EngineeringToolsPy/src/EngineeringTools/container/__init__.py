#!/usr/bin/env python3
# pylint: disable-msg=line-too-long,missing-module-docstring,missing-function-docstring,missing-class-docstring,no-else-return,invalid-name,multiple-statements

__author__  = 'Martin Hochwallner <marthoch@users.noreply.github.com>'
__email__   = "marthoch@users.noreply.github.com"
__license__ = "BSD 3-clause"

# $Source$

from .. import quantities as ETQ


class Obj:
    def __str__(self):
        return '\n' + '\n'.join(['{:20s} = {:s}'.format(k, v) for k, v in vars(self).iteritems()])

    def _repr_html_(self):
        #html = """<font face="monospace">\n"""
        html = """<table border="1">\n"""
        for  k, v in vars(self).items():
            if isinstance(v, Obj):
                html += """<tr>
<td>{:s}</td>
<td>{:s}</td>
</tr>
""".format(k, v._repr_html_())

            elif isinstance(v, ETQ.Quantity):
                html += """<tr>
<td>{:s}</td>
<td style="text-align:left">{:s}</td>
</tr>
""".format(k, v._repr_html_())

            else:
                html += """<tr>
<td>{:s}</td>
<td>{:s}</td>
</tr>
""".format(k, str(v).replace('\n', '<br>'))
        html += """</table>
</font>\n"""
        return html


    def to_dict(self, flat=False, sep='::', prefix=None):
        """Return the data in the object ad dict.
        flat=True: flatten if object contains object.
        """
        d = {}
        for  k, v in vars(self).items():
            if prefix:
                k = '{}{}{}'.format(prefix, sep, k)
            if isinstance(v, Obj):
                if flat:
                    d.update(v.to_dict(flat=True, sep=sep, prefix=k))
                else:
                    d[k] = v.to_dict()
            else:
                d[k] = v
        return d



class REQ:

    def __init__(self, text=None):
        self.text = text

    def __str__(self):
        return self.text.format(self)

    __repr__ = __str__

    def _repr_html_(self):
        return "<h1>" + str(self) + "</h1>"


#eof
