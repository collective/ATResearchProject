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

__old_name__ = 'Products.ATResearchProject.ResearchField'

import re

from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from AccessControl import ClassSecurityInfo
from zope.interface import implements
from OFS.interfaces import IItem
try:
  from Products.LinguaPlone.public import BaseContent
  from Products.LinguaPlone.public import registerType

except:
  from Products.Archetypes.public import BaseContent
  from Products.Archetypes.public import registerType
 
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.ATResearchProject.config import PROJECTNAME
from Products.ATResearchProject.config import ATRP_TOOL_ID
from Products.ATResearchProject.config import ALLOWED_CT_DEFAULTS

from schemata import ATResearchFieldSchema
from Products.ATResearchProject.utils import _encode, _decode
"""
ResearchField.py: Content type to store referencable research field information.
"""

class ResearchField(BrowserDefaultMixin, BaseContent):
    """Content type for characterizing research fields.
    """

    implements(IItem)

    content_icon    = 'research_field_icon.gif'
    meta_type       = 'ATResearchField'
    portal_type     = 'ResearchField'
    archetype_name  = 'Research Field'
    default_view    = 'research_field_view'
    immediate_view  = 'research_field_view'
    assocMimetypes  = ('application/xhtml+xml','message/rfc822','text/*')
    
    typeDescription = ("Use this content type to depict your institute's research fields. Afterwards, research projects and subprojects can easily reference existing research fields.")
    typeDescMsgId   = 'description_edit_researchfield'
    
    security = ClassSecurityInfo()
    
    schema = ATResearchFieldSchema

    actions = (
            { 'id': 'view',
              'name': 'View',
              'action': 'string:${object_url}/research_field_view',
	      'permissions': (permissions.View),
            },    
            {
              'id'          : 'edit',
	      'name'        : 'Edit',
	      'action'      : 'string:${object_url}/edit',
	      'permissions' : (permissions.ModifyPortalContent,),
	    },
            { 'id': 'external_edit',
              'name': 'External Edit',
	      'action': 'string:${object_url}/external_edit',
	      'condition': 'object/externalEditorEnabled',
	      'permissions': (permissions.ModifyPortalContent,),
	      'visible': 0,
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

    security.declareProtected(permissions.View, 'getResearchFieldRefFieldEntry')
    def getResearchFieldRefFieldEntry(self):
      """Generate a custom vocabulary entry if a research field should get referenced within 
      research projects."""
      putils = getToolByName(self, 'plone_utils', None)
      navtool = getToolByName(self, 'portal_properties', None).navtree_properties
      filter_wf = navtool and navtool.getProperty('enable_wf_state_filtering', False)
      wftool = getToolByName(self, 'portal_workflow')
      reviewstate = wftool.getInfoFor(self, 'review_state')
      if not(navtool and wftool) or (reviewstate in navtool.wf_states_to_show):
        return '%s - %s (/%s)' % (_decode(putils.pretty_title_or_id(self)), _decode(self.Description()), self.virtual_url_path())
      else:
        return '%s: %s - %s (/%s)' % (self.translate(putils.getReviewStateTitleFor(self)), _decode(putils.pretty_title_or_id(self)), _decode(self.Description()), self.virtual_url_path())
		 
    security.declareProtected(permissions.View, 'getResearchFieldExternalLinks')
    def getResearchFieldExternalLinks (self, **kwargs):
        """we need to wrap this field as the user is allowed to enter extended text infomation
        """
        atrp_tool = getToolByName(self, 'portal_researchproject')
        raw_external_links = self.getField('researchFieldExternalLinks').get(self, **kwargs)
        external_links_list = []
        # detect the output format for the lines in the LinesField
        if kwargs.get('extended_field_format', False):
            formatType = kwargs.get('extended_field_format')
        else:
	    formatType = 'raw'
	
	for external_link in raw_external_links:
	    if re.match('.*<url:.*>$', external_link) or (formatType in ['plain', 'raw']):
	        external_links_list.append(external_link)
	    else:
	        external_links_list.append('%s <url:%s>' % (external_link, external_link))
	
	return atrp_tool.structureExtendedLinesField(external_links_list,**kwargs)
                                                                                                                                
registerType(ResearchField,PROJECTNAME)
