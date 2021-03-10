#!/usr/bin/env python3
# pylint: disable-msg=line-too-long,missing-module-docstring,missing-function-docstring,missing-class-docstring,no-else-return,invalid-name,multiple-statements

__author__  = 'Martin Hochwallner <marthoch@users.noreply.github.com>'
__email__   = "marthoch@users.noreply.github.com"
__license__ = "BSD 3-clause"

# $Source$

import numpy as _np
from .. import quantities as ETQ


class Obj:

    def __init__(self, name=None):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def __format__(self, format_spec):
        return self.__str__()

    def get_variables(self):
        return {key: value for key, value in vars(self).items() if not key.startswith('_')}

    def __str__(self):
        variables = self.get_variables()
        txt = ''
        if self._name:
            if isinstance(self._name, ETQ.String):
                txt += '{}:  \n'.format(self._name.value.format(self=self))
            else:
                txt += '{}:  \n'.format(self._name.format(self=self))
        txt += '\n'.join(['{:20s} = {:s}'.format(k, v if v else 'None') for k, v in variables.items()])
        return txt


    def _repr_html_(self):
        #html = """<font face="monospace">\n"""
        html = ''
        if self._name:
            if isinstance(self._name, ETQ.String):
                html += '<h4 style="text-align:left">{} </h4> \n'.format(self._name.value.format(self=self))
            else:
                html += '<h4 style="text-align:left">{} </h4> \n'.format(self._name.format(self=self))
        html += """<table border="1">\n"""
        for  k, v in self.get_variables().items():
            if isinstance(v, Obj):
                html += """<tr>
<td valign="top">{:s}</td>
<td>{:s}</td>
</tr>
""".format(k, v._repr_html_())

            elif isinstance(v, ETQ.Quantity):
                html += """<tr>
<td valign="top">{:s}</td>
<td style="text-align:left">{:s}</td>
</tr>
""".format(k, v._repr_html_())
            elif isinstance(v, (list, _np.ndarray)) and isinstance(v[0], ETQ.Quantity):
                txt = [vv._repr_html_() for vv in v]
                txt = '<br>'.join(txt)
                html += """<tr>
<td valign="top">{:s}</td>
<td style="text-align:left">{:s}</td>
</tr>
""".format(k, txt)
            else:
                html += """<tr>
<td valign="top">{:s}</td>
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
        for  k, v in self.get_variables().items():
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



class REQ(Obj):

    def __init__(self, text=None, reqid=None):
        super().__init__(None)
        self._text = text
        self._reqid = reqid

    @property
    def reqid(self):
        return self._reqid

    @property
    def text(self):
        return self._text

    def __str__(self):
        txt = ''
        if self._reqid:
            txt += '{}: '.format(self._reqid)
        txt += self.text.format(self=self)
        return txt

    __repr__ = __str__

    def _repr_html_(self):
        txt = '<h4 style="text-align:left"> '
        if self._reqid:
            txt += '{}: '.format(self._reqid)
        txt += self._text.format(self=self)
        txt += "</h4> \n"
        txt += super()._repr_html_()
        return txt

#eof
