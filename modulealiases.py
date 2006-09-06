#  This program is free software; you can redistribute it and/or modify
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
#  This module is derived from ATContentTypes/modulaliases.py
#

"""Module aliases for unpickling

The dotted class path of most persistent classes were before version 0.3.6rc4. 
This module creates aliases using sys.modules for unpickling old objects.
"""

import sys
from types import ModuleType

from Products.ATResearchProject.content import ResearchProject
from Products.ATResearchProject.content import ResearchSubproject
from Products.ATResearchProject.content import ResearchProjectList
from Products.ATResearchProject.content import ResearchProjectInternalFolder
from Products.ATResearchProject.content import ResearchField

def createModuleAliases():
    """Creates module aliases in sys.modules
    
    Aliases are created for Products.ATResearchProject modules which contain 
    classes with persistent objects (content types).
    
    It might look a little bit tricky but it's very easy. The method is
    iterating over all modules in the module name space (globals) and creating
    aliases only forthoses modules which are modules with the module name starting with
    Products.ATContentTypes. All these modules have a module level var called
    "__old_name__".
    """
    for module in globals().values():
        if type(module) is not ModuleType:
            # not a module
            continue
        name = module.__name__
        if not name.startswith('Products.ATResearchProject'):
            # not a module inside ATCT
            continue
        old_name = getattr(module, '__old_name__', None)
        if old_name is None:
            continue
        sys.modules[old_name] = module

createModuleAliases()
