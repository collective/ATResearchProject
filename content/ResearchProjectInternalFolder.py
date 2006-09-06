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

__old_name__ = 'Products.ATResearchProject.ResearchProjectInternalFolder'

import copy

from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from AccessControl import ClassSecurityInfo

try:
  from Products.LinguaPlone.public import OrderedBaseFolder
  from Products.LinguaPlone.public import registerType

except:
  from Products.Archetypes.public import OrderedBaseFolder
  from Products.Archetypes.public import registerType
 
from Products.ATContentTypes.atct import ATFolder
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.ATResearchProject.config import PROJECTNAME
from Products.ATResearchProject.config import ALLOWED_CT_DEFAULTS

"""
ResearchProjectFolder.py: really simple content type using OrderedBaseFolder schema
"""

class ResearchProjectInternalFolder(ATFolder):
    """Content type to be used as a normal folder within research projects.
       Only difference from ATFolder is the list of allowed_content_types. 
    """

    __implements__ = (ATFolder.__implements__,
		     )

    security = ClassSecurityInfo()

    meta_type       = 'ATResearchProjectInternalFolder'
    portal_type     = 'ResearchProjectInternalFolder'
    archetype_name  = 'Folder'
    immediate_view  = 'folder_listing'
    suppl_views      = ('folder_listing', 'folder_summary_view', 'folder_tabular_view','research_subprojects_overview',)

    actions = (
        { 'id': 'view',
          'name': 'View',
          'action': 'string:${folder_url}/',
          'permissions': (permissions.View),
        },
        {
          'id'          : 'edit',
	  'name'        : 'Edit',
	  'action'      : 'string:${object_url}/edit',
	  'permissions' : (permissions.ModifyPortalContent,),
	},
	{
	  'id': 'local_roles',
	  'name': 'Sharing',
	  'action': 'string:${object_url}/folder_localrole_form',
	  'permissions': (permissions.ManageProperties,),
          'condition': 'python: object.portal_membership.checkPermission("ManageProperties", object)',
	},
    )

    aliases = {
        '(Default)'  : '(dynamic view)',
        'view'       : '(selected layout)',
        'index.html' : '(dynamic view)',
        'edit'       : 'base_edit',
        'properties' : 'base_metadata',
        'sharing'    : 'folder_localrole_form',
        'gethtml'    : '',
        'mkdir'      : '',
    }
									
    factory_type_information = {
        'allow_discussion': 0,
        'immediate_view': 'folder_listing',
        'global_allow': 0,
        'allowed_content_types': ALLOWED_CT_DEFAULTS['allowed_content_types_researchprojectinternalfolder'],
    	'filter_content_types': 1,
    }
        
registerType(ResearchProjectInternalFolder,PROJECTNAME)
