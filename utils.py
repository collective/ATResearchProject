#  This program is free software; you can redistribute it and/or modify6
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
"""ATResearchProject utitility lib"""

## a poor-mans approach to fixing unicode issues :-(
_default_charset = 'utf-8'

# Python stuff
import re, string, types
from types import UnicodeType

def _encode(s, encoding=_default_charset, obj=None):

    if obj and obj.hasProperty('default_charset'):
        encoding=obj.getProperty('default_charset')

    try:
        return s.encode(encoding)
    except (TypeError, UnicodeDecodeError, ValueError):
        return s
    
def _decode(s, encoding=_default_charset, obj=None, ):

    if obj and obj.hasProperty('default_charset'):
        encoding=obj.getProperty('default_charset')

    try:
        return unicode(s, encoding)
    except (TypeError, UnicodeDecodeError, ValueError):
        return s

