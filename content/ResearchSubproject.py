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

__old_name__ = 'Products.ATResearchProject.ResearchSubproject'

from types import StringType
import re

try:
    from Products.LinguaPlone.public import OrderedBaseFolder, registerType

except ImportError:
    # No multilingual support
    from Products.Archetypes.public import OrderedBaseFolder, registerType

from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from AccessControl import ClassSecurityInfo

from Products.ATResearchProject.config import PROJECTNAME
from Products.ATResearchProject.config import SUBPROJECT_INFOFIELD_ACCESSORS
from Products.ATResearchProject.config import ATRP_TOOL_ID
from Products.ATResearchProject.config import ALLOWED_CT_DEFAULTS
from Products.ATResearchProject.config import INFINITY

from schemata import ATResearchSubprojectSchema

class ResearchSubproject(BrowserDefaultMixin, OrderedBaseFolder):
    """Folderish content type to hold information on a scientific subproject that is situated in a research project folder.
    """

    __implements__ = (OrderedBaseFolder.__implements__,
                      BrowserDefaultMixin.__implements__,
		     ) 
                     
    implicitly_addable = False		     
    content_icon    = 'research_subproject_icon.gif'
    meta_type       = 'ATResearchSubproject'
    portal_type     = 'ResearchSubproject'
    archetype_name  = 'Subproject'
    default_view    = 'research_subproject_view'
    immediate_view  = 'research_subproject_view'
    assocMimetypes  = ('application/xhtml+xml', 'message/rfc822', 'text/*')
    
    typeDescMsgId   = 'description_edit_researchsubproject'
    typeDescription = 'A subproject folder offers the possbility to substructure a research project. ' + \
                      'This folderish content type is only available within research project folders.'

    schema          = ATResearchSubprojectSchema

    security        = ClassSecurityInfo()
    
    actions = (
	{
	'id': 'view',
        'name': 'View',
        'action': 'string:${object_url}/research_subproject_view',
        'permissions': (permissions.View,),
	},
	{
        'id'          : 'edit',
        'name'        : 'Edit',
        'action'      : 'string:${object_url}/edit',
        'permissions' : (permissions.ModifyPortalContent,),
        },
	{
	'id': 'external_edit',
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

    factory_type_information = {
            'allow_discussion': 0,
            'immediate_view': 'base_view',
            'global_allow': 0,
	    'allowed_content_types': ALLOWED_CT_DEFAULTS['allowed_content_types_subproject'],
	    'filter_content_types': 1,
    }

    security.declareProtected(permissions.View, 'getFieldValue')
    def getFieldValue (self, accessor=None, **kwargs):
      """get any field value we know the accessor of
      """
      try:
        if type(accessor) is StringType:
          return eval('self.%s(**kwargs)' % accessor)
      except AttributeError:
        pass

      return None

    security.declareProtected(permissions.View, 'getResearchSubprojectInfoFields')
    def getResearchSubprojectInfoFields (self, **kwargs):
      """get all subproject information fields
      """
      rsp_info = []
      for accessor in SUBPROJECT_INFOFIELD_ACCESSORS:
        rsp_info.extend(eval('self.%s(**kwargs)' % accessor))

      return rsp_info
					      
    security.declareProtected(permissions.ModifyPortalContent, 'setResearchSubprojectOfficialTitleAndTitle')
    def setResearchSubprojectOfficialTitleAndTitle (self, value, **kwargs):
        """Duplicate Title into researchSubprojectTitle.
        """
        self.researchSubprojectTitle = value
        self.getField('title').set(self, value, **kwargs)
        
    security.declareProtected(permissions.ModifyPortalContent, 'setResearchSubprojectOfficialTitleAndDescription')
    def setResearchSubprojectOfficialTitleAndDescription (self, value, **kwargs):
        """Duplicate description attribute into researchSubprojectOfficialTitle attribute. This method is set as the
           mutator for field description.
        """
        self.researchSubprojectOfficialTitle = value
        self.getField('description').set(self, value, **kwargs)
                          
    security.declareProtected(permissions.View, 'getAuthors')
    def getAuthors (self, **kwargs):
      """we need to wrap this field as the user is allowed to enter extended text infomation
      """
      atrp_tool = getToolByName(self, 'portal_researchproject')
      raw_authors_field = self.getField('authors').get(self, **kwargs)
      return atrp_tool.structureExtendedLinesField(raw_authors_field,**kwargs)

    security.declareProtected(permissions.View, 'getResearchProjectRuntimeStart')
    def getResearchProjectRuntimeStart (self, **kwargs):
      """we explicitly need this method for a subproject's runtime field's getDefault
      """
      rp_object = self.getResearchProjectObject()      
      return rp_object.getResearchProjectRuntimeStart(**kwargs)

    security.declareProtected(permissions.View, 'getResearchProjectRuntimeEnd')
    def getResearchProjectRuntimeEnd (self, **kwargs):
      """we explicitly need this method for a subproject's runtime field's getDefault() method
      """
      rp_object = self.getResearchProjectObject()      
      return rp_object.getResearchProjectRuntimeEnd(**kwargs)

    security.declareProtected(permissions.ModifyPortalContent, 'setResearchSubprojectRuntimeEnd')
    def setResearchSubprojectRuntimeEnd (self, value, **kwargs):
      """we need to wrap this field for open ended projects
      """
      if not value:
        value = INFINITY
    
      self.getField('researchSubprojectRuntimeEnd').set(self, value, **kwargs)
                                
    security.declareProtected(permissions.View, 'getResearchSubprojectRuntimeEnd')
    def getResearchSubprojectRuntimeEnd (self, **kwargs):
      """we need to wrap this field for open ended subprojects
      """
      rawFieldValue = self.getField('researchSubprojectRuntimeEnd').get(self, **kwargs)
      if str(rawFieldValue) == INFINITY:
        return None

      return rawFieldValue

    security.declareProtected(permissions.View, 'getResearchSubprojectScientificCoordinators')
    def getResearchSubprojectScientificCoordinators (self, **kwargs):
      """we need to wrap this field as the user is allowed to enter extended text infomation
      """
      atrp_tool = getToolByName(self, 'portal_researchproject')
      rawFieldValue = self.getField('researchSubprojectScientificCoordinators').get(self, **kwargs)
      return atrp_tool.structureExtendedLinesField(rawFieldValue,**kwargs)

    security.declareProtected(permissions.View, 'getResearchSubprojectScientificStaffMembers')
    def getResearchSubprojectScientificStaffMembers (self, **kwargs):
      """we need to wrap this field as the user is allowed to enter extended text infomation
      """
      atrp_tool = getToolByName(self, 'portal_researchproject')
      rawFieldValue = self.getField('researchSubprojectScientificStaffMembers').get(self, **kwargs)
      return atrp_tool.structureExtendedLinesField(rawFieldValue,**kwargs)

    security.declareProtected(permissions.View, 'getResearchSubprojectTechnicalStaffMembers')
    def getResearchSubprojectTechnicalStaffMembers (self, **kwargs):
      """we need to wrap this field as the user is allowed to enter extended text infomation
      """
      atrp_tool = getToolByName(self, 'portal_researchproject')
      rawFieldValue = self.getField('researchSubprojectTechnicalStaffMembers').get(self, **kwargs)
      return atrp_tool.structureExtendedLinesField(rawFieldValue,**kwargs)

    security.declareProtected(permissions.View, 'getResearchSubprojectStudentStaffMembers')
    def getResearchSubprojectStudentStaffMembers (self, **kwargs):
      """we need to wrap this field as the user is allowed to enter extended text infomation
      """
      atrp_tool = getToolByName(self, 'portal_researchproject')
      rawFieldValue = self.getField('researchSubprojectStudentStaffMembers').get(self, **kwargs)
      return atrp_tool.structureExtendedLinesField(rawFieldValue,**kwargs)

    security.declareProtected(permissions.View, 'getResearchSubprojectFormerStaffMembers')
    def getResearchSubprojectFormerStaffMembers (self, **kwargs):
      """we need to wrap this field as the user is allowed to enter extended text infomation
      """
      atrp_tool = getToolByName(self, 'portal_researchproject')
      rawFieldValue = self.getField('researchSubprojectFormerStaffMembers').get(self, **kwargs)
      return atrp_tool.structureExtendedLinesField(rawFieldValue,**kwargs)

    security.declareProtected(permissions.View, 'getResearchSubprojectFormerStudentStaffMembers')
    def getResearchSubprojectFormerStudentStaffMembers (self, **kwargs):
      """we need to wrap this field as the user is allowed to enter extended text infomation
      """
      atrp_tool = getToolByName(self, 'portal_researchproject')
      rawFieldValue = self.getField('researchSubprojectFormerStudentStaffMembers').get(self, **kwargs)
      return atrp_tool.structureExtendedLinesField(rawFieldValue,**kwargs)

    security.declareProtected(permissions.View, 'getResearchSubprojectInheritedScientificStaffMembers')
    def getResearchSubprojectInheritedScientificStaffMembers (self, **kwargs):
        """acquire all sublevel subprojects' scientific staff members
        """
        atrp_tool = getToolByName(self, 'portal_researchproject')
        if self.getResearchSubprojectInheritScientificStaffMembers():
            raw_staff_members_list = list(self.getField('researchSubprojectScientificStaffMembers').get(self, **kwargs))
            subproject_objects = atrp_tool.listWfFilteredResearchSubprojects(self)
            for subproject_object in subproject_objects:
                for line in subproject_object.getResearchSubprojectScientificStaffMembers():
                    
                    # this bit of code has to be more versatile, filter multiple staff member names regardless of title etc.
                    # make it a tool method!!!
                    if atrp_tool.structureExtendedLinesField([line], extended_field_format='plain')[0] not in atrp_tool.structureExtendedLinesField(raw_staff_members_list, extended_field_format='plain'):
                        raw_staff_members_list.append(line)
        else:
            raw_staff_members_list = self.getField('researchSubprojectScientificStaffMembers').get(self, **kwargs)
        return atrp_tool.structureExtendedLinesField(raw_staff_members_list,**kwargs)

    security.declareProtected(permissions.View, 'getResearchSubprojectInheritedTechnicalStaffMembers')
    def getResearchSubprojectInheritedTechnicalStaffMembers (self, **kwargs):
        """acquire all sublevel subprojects' technical staff members
        """
        atrp_tool = getToolByName(self, 'portal_researchproject')
        if self.getResearchSubprojectInheritTechnicalStaffMembers():
            raw_staff_members_list = list(self.getField('researchSubprojectTechnicalStaffMembers').get(self, **kwargs))
            subproject_objects = atrp_tool.listWfFilteredResearchSubprojects(self)
            for subproject_object in subproject_objects:
                for line in subproject_object.getResearchSubprojectTechnicalStaffMembers():
        
                    # this bit of code has to be more versatile, filter multiple staff member names regardless of title etc.
                    # make it a tool method!!!
                    if atrp_tool.structureExtendedLinesField([line], extended_field_format='plain')[0] not in atrp_tool.structureExtendedLinesField(raw_staff_members_list, extended_field_format='plain'):
                        raw_staff_members_list.append(line)
        else:
            raw_staff_members_list = self.getField('researchSubprojectTechnicalStaffMembers').get(self, **kwargs)
        return atrp_tool.structureExtendedLinesField(raw_staff_members_list,**kwargs)

    security.declareProtected(permissions.View, 'getResearchSubprojectInheritedStudentStaffMembers')
    def getResearchSubprojectInheritedStudentStaffMembers (self, **kwargs):
        """acquire all sublevel subprojects' student staff members
        """
        atrp_tool = getToolByName(self, 'portal_researchproject')
        if self.getResearchSubprojectInheritStudentStaffMembers():
            raw_staff_members_list = list(self.getField('researchSubprojectStudentStaffMembers').get(self, **kwargs))
            subproject_objects = atrp_tool.listWfFilteredResearchSubprojects(self)
            for subproject_object in subproject_objects:
                for line in subproject_object.getResearchSubprojectStudentStaffMembers():
        
                    # this bit of code has to be more versatile, filter multiple staff member names regardless of title etc.
                    # make it a tool method!!!
                    if atrp_tool.structureExtendedLinesField([line], extended_field_format='plain')[0] not in atrp_tool.structureExtendedLinesField(raw_staff_members_list, extended_field_format='plain'):
                        raw_staff_members_list.append(line)
        else:
            raw_staff_members_list = self.getField('researchSubprojectStudentStaffMembers').get(self, **kwargs)
        return atrp_tool.structureExtendedLinesField(raw_staff_members_list,**kwargs)

    security.declareProtected(permissions.View, 'getResearchSubprojectInheritedFormerStaffMembers')
    def getResearchSubprojectInheritedFormerStaffMembers (self, **kwargs):
        """acquire all sublevel subprojects' former staff members
        """
        atrp_tool = getToolByName(self, 'portal_researchproject')
        if self.getResearchSubprojectInheritFormerStaffMembers():
            raw_staff_members_list = list(self.getField('researchSubprojectFormerStaffMembers').get(self, **kwargs))
            subproject_objects = atrp_tool.listWfFilteredResearchSubprojects(self)
            for subproject_object in subproject_objects:
                for line in subproject_object.getResearchSubprojectFormerStaffMembers():
        
                    # this bit of code has to be more versatile, filter multiple staff member names regardless of title etc.
                    # make it a tool method!!!
                    if atrp_tool.structureExtendedLinesField([line], extended_field_format='plain')[0] not in atrp_tool.structureExtendedLinesField(raw_staff_members_list, extended_field_format='plain'):
                        raw_staff_members_list.append(line)
        else:
            raw_staff_members_list = self.getField('researchSubprojectFormerStaffMembers').get(self, **kwargs)
        return atrp_tool.structureExtendedLinesField(raw_staff_members_list,**kwargs)

    security.declareProtected(permissions.View, 'getResearchSubprojectInheritedFormerStudentStaffMembers')
    def getResearchSubprojectInheritedFormerStudentStaffMembers (self, **kwargs):
        """acquire all sublevel subprojects' former student staff members
        """
        atrp_tool = getToolByName(self, 'portal_researchproject')
        if self.getResearchSubprojectInheritFormerStudentStaffMembers():
            raw_staff_members_list = list(self.getField('researchSubprojectFormerStudentStaffMembers').get(self, **kwargs))
            subproject_objects = atrp_tool.listWfFilteredResearchSubprojects(self)
            for subproject_object in subproject_objects:
                for line in subproject_object.getResearchSubprojectFormerStudentStaffMembers():
        
                    # this bit of code has to be more versatile, filter multiple staff member names regardless of title etc.
                    # make it a tool method!!!
                    if atrp_tool.structureExtendedLinesField([line], extended_field_format='plain')[0] not in atrp_tool.structureExtendedLinesField(raw_staff_members_list, extended_field_format='plain'):
                        raw_staff_members_list.append(line)
        else:
            raw_staff_members_list = self.getField('researchSubprojectFormerStudentStaffMembers').get(self, **kwargs)
        return atrp_tool.structureExtendedLinesField(raw_staff_members_list,**kwargs)

    security.declareProtected(permissions.View, 'getResearchSubprojectExternalInstitutes')
    def getResearchSubprojectExternalInstitutes (self, **kwargs):
      """we need to wrap this field as the user is allowed to enter extended text infomation
      """
      atrp_tool = getToolByName(self, 'portal_researchproject')
      rawFieldValue = self.getField('researchSubprojectExternalInstitutes').get(self, **kwargs)
      return atrp_tool.structureExtendedLinesField(rawFieldValue,**kwargs)

    security.declareProtected(permissions.View, 'getResearchSubprojectCooperationPartners')
    def getResearchSubprojectCooperationPartners (self, **kwargs):
      """we need to wrap this field as the user is allowed to enter extended text infomation
      """
      atrp_tool = getToolByName(self, 'portal_researchproject')
      rawFieldValue = self.getField('researchSubprojectCooperationPartners').get(self, **kwargs)
      return atrp_tool.structureExtendedLinesField(rawFieldValue,**kwargs)

    security.declareProtected(permissions.View, 'getResearchSubprojectExternalLinks')
    def getResearchSubprojectExternalLinks (self, **kwargs):
	"""we need to wrap this field as the user is allowed to enter extended text infomation
	"""
	atrp_tool = getToolByName(self, 'portal_researchproject')
	raw_external_links = self.getField('researchSubprojectExternalLinks').get(self, **kwargs)
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
																				          
    security.declareProtected(permissions.View, 'getResearchSubprojectInvolvedDepartmentsLongname')
    def getResearchSubprojectInvolvedDepartmentsLongname(self, **kwargs):
        """
        Get the long name of the department from the research project site configuration tool
        """
        involvedDepartmentIDs = self.getResearchSubprojectInvolvedDepartments()
        if hasattr (self, ATRP_TOOL_ID):
				
	    atrp_tool = getToolByName(self, ATRP_TOOL_ID)
            involvedDepartmentLongnames = []
				    
	    for id in involvedDepartmentIDs:
	      involvedDepartmentLongnames.append(atrp_tool.getDepartmentLongnameById(id))
	    
	    return involvedDepartmentLongnames
	
	else:
	    return involvedDepartmentIDs
														      				   
    security.declareProtected(permissions.View, 'getSuperiorResearchSubprojectObject')
    def getSuperiorResearchSubprojectObject(self, **kwargs):
        """
        Make the object instance of a superior research subproject (if any) known to the current subproject without much hassle...
        """
        obj = self.aq_inner.aq_parent
        while 1:
            if obj.portal_type == 'ResearchSubproject':
                break
            elif (obj.portal_type == 'ResearchProject') or (obj.portal_type == 'PloneSite'):
                obj = None
                break    
            else:
                obj = obj.aq_inner.aq_parent
        
        return obj
                                                                                                    
    security.declareProtected(permissions.View, 'getSuperiorResearchSubprojectUrl')
    def getSuperiorResearchSubprojectUrl(self, **kwargs):
        """
        Make the URL of the next superior subproject known to the current subproject children without much hassle...
        """
        superior_obj = self.getSuperiorResearchSubprojectObject()

        if superior_obj:
            return superior_obj.absolute_url(**kwargs)

        return None

    security.declarePrivate('at_post_create_script')
    def at_post_create_script(self):
	self.at_post_edit_script(self):

    security.declarePrivate('at_post_edit_script')
    def at_post_edit_script(self):
    
	self.reindexSuperiorRPandRSPobjects()
    
    def __bobo_traverse__(self, REQUEST, name):
	"""
	Transparent access to logo scales
	"""
	if name.startswith('logo'):
	    field = self.getField('logo')
	    logo = None
	    if name == 'logo':
	        figure = field.getScale(self)
	    else:
	        scalename = name[len('logo_'):]
	        if scalename in self.getAvailableLogoSizes().keys():
                  logo = field.getScale(self, scale=scalename)
            if logo is not None and not isinstance(logo, basestring):
                return figure
	
	return OrderedBaseFolder.__bobo_traverse__(self, REQUEST, name)
																									    #def allowedContentTypes(self):
    #  """
    #  restrict allowed content types to a dedicated list of ctypes
    #  """
    #  _all_allowed_ctypes = [ ctype for ctype in OrderedBaseFolder.allowedContentTypes(self) ]
    #  return [ ctype for ctype in _all_allowed_ctypes if ctype.getId() in self.allowed_types ]
	    										
registerType(ResearchSubproject, PROJECTNAME)