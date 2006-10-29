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

__old_name__ = 'Products.ATResearchProject.ResearchProject'

import copy, re

from types import StringType

from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from AccessControl import ClassSecurityInfo

try:
  from Products.LinguaPlone.public import OrderedBaseFolder
  from Products.LinguaPlone.public import registerType

except:
  from Products.Archetypes.public import OrderedBaseFolder
  from Products.Archetypes.public import registerType
 
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.ATResearchProject.config import PROJECTNAME
from Products.ATResearchProject.config import PROJECT_INFOFIELD_ACCESSORS
from Products.ATResearchProject.config import ATRP_TOOL_ID
from Products.ATResearchProject.config import ALLOWED_CT_DEFAULTS
from Products.ATResearchProject.config import INFINITY

from schemata import ATResearchProjectSchema

"""
ResearchProjectFolder.py: really simple content type using OrderedBaseFolder schema
"""

class ResearchProject(BrowserDefaultMixin, OrderedBaseFolder):
    """Folderish content type for characterizing research projects.
    """

    __implements__ = (OrderedBaseFolder.__implements__,
                      BrowserDefaultMixin.__implements__,
		     )

    content_icon    = 'research_project_icon.gif'
    meta_type       = 'ATResearchProject'
    portal_type     = 'ResearchProject'
    archetype_name  = 'Research Project'
    default_view    = 'research_project_view'
    immediate_view  = 'research_project_view'
    assocMimetypes  = ('application/xhtml+xml','message/rfc822','text/*')
    
    typeDescription = ("Use this folderish content type to characterize research projects. Research projects can contain only a limited set of contain types.")
    typeDescMsgId   = 'description_edit_researchproject'
    
    description     = ''
    
    security = ClassSecurityInfo()
    
    schema = ATResearchProjectSchema

    factory_type_information = {
        'allow_discussion': 0,
        'immediate_view': 'base_view',
        'global_allow': 1,
        'allowed_content_types': ALLOWED_CT_DEFAULTS['allowed_content_types_researchproject'],
	'filter_content_types': 1,
    }
        
    actions = (
            { 'id': 'view',
              'name': 'View',
              'action': 'string:${object_url}/research_project_view',
	      'permissions': (permissions.View),
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
	'edit'	     : 'base_edit',
        'properties' : 'base_metadata',
        'sharing'    : 'folder_localrole_form',
        'gethtml'    : '',
        'mkdir'      : '',
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

    security.declareProtected(permissions.View, 'getResearchProjectInfoFields')
    def getResearchProjectInfoFields (self, **kwargs):
      """get all project information fields
      """
      rp_info = []
      for accessor in PROJECT_INFOFIELD_ACCESSORS:
        rp_info.extend(eval('self.%s(**kwargs)' % accessor))
      return rp_info

    security.declareProtected(permissions.ModifyPortalContent, 'setResearchProjectOfficialTitleAndTitle')
    def setResearchProjectOfficialTitleAndTitle (self, value, **kwargs):
      """Duplicate Title into researchProjectTitle.
      """
      self.researchProjectTitle = value
      self.getField('title').set(self, value, **kwargs)

    security.declareProtected(permissions.ModifyPortalContent, 'setResearchProjectOfficialTitleAndDescription')
    def setResearchProjectOfficialTitleAndDescription (self, value, **kwargs):
      """Duplicate researchProjectOfficialTitle into description property. This method is set as the 
      mutator for researchProjectOfficialTitle.
      """
      self.description = value
      self.getField('researchProjectOfficialTitle').set(self, value, **kwargs)

    security.declareProtected(permissions.View, 'getDescription')
    def getDescription (self, **kwargs):
      """Return value of virtual description property (mutated via setResearchProjectOfficialTitleAndDescription).
      """
      return self.getResearchProjectOfficialTitle(**kwargs)

    security.declareProtected(permissions.View, 'Description')
    def Description (self, **kwargs):
      """Alias for class.getDescription.
      """
      return self.getDescription(**kwargs)

    security.declareProtected(permissions.View, 'getAuthors')
    def getAuthors (self, **kwargs):
        """we need to wrap this field as the user is allowed to enter extended text infomation
        """
        atrp_tool = getToolByName(self, 'portal_researchproject')
        raw_authors_list = self.getField('authors').get(self, **kwargs)
        return atrp_tool.structureExtendedLinesField(raw_authors_list,**kwargs)
      
    security.declareProtected(permissions.ModifyPortalContent, 'setResearchProjectRuntimeEnd')
    def setResearchProjectRuntimeEnd (self, value, **kwargs):
      """we need to wrap this field for open ended projects
      """
      if not value:
        value = INFINITY    
      self.getField('researchProjectRuntimeEnd').set(self, value, **kwargs)
      
    security.declareProtected(permissions.View, 'getResearchProjectRuntimeEnd')
    def getResearchProjectRuntimeEnd (self, **kwargs):
      """we need to wrap this field for open ended projects
      """
      rawFieldValue = self.getField('researchProjectRuntimeEnd').get(self, **kwargs)
      if str(rawFieldValue) == INFINITY:
        return None
        
      return rawFieldValue
      
    security.declareProtected(permissions.View, 'getResearchProjectProjectCoordinators')
    def getResearchProjectProjectCoordinators (self, **kwargs):
      """we need to wrap this field as the user is allowed to enter extended text infomation
      """
      atrp_tool = getToolByName(self, 'portal_researchproject')
      rawFieldValue = self.getField('researchProjectProjectCoordinators').get(self, **kwargs)
      return atrp_tool.structureExtendedLinesField(rawFieldValue,**kwargs)
      
    security.declareProtected(permissions.View, 'getResearchProjectProjectCoordinators')
    def getResearchProjectProjectCoordinators (self, **kwargs):
      """we need to wrap this field as the user is allowed to enter extended text infomation
      """
      atrp_tool = getToolByName(self, 'portal_researchproject')
      rawFieldValue = self.getField('researchProjectProjectCoordinators').get(self, **kwargs)
      return atrp_tool.structureExtendedLinesField(rawFieldValue,**kwargs)
      
    security.declareProtected(permissions.View, 'getResearchProjectScientificCoordinators')
    def getResearchProjectScientificCoordinators (self, **kwargs):
      """we need to wrap this field as the user is allowed to enter extended text infomation
      """
      atrp_tool = getToolByName(self, 'portal_researchproject')
      rawFieldValue = self.getField('researchProjectScientificCoordinators').get(self, **kwargs)
      return atrp_tool.structureExtendedLinesField(rawFieldValue,**kwargs)
      
    security.declareProtected(permissions.View, 'getResearchProjectContactPersons')
    def getResearchProjectContactPersons(self, **kwargs):
      """we need to wrap this field as the user is allowed to enter extended text infomation
      """
      atrp_tool = getToolByName(self, 'portal_researchproject')
      rawFieldValue = self.getField('researchProjectContactPersons').get(self, **kwargs)
      return atrp_tool.structureExtendedLinesField(rawFieldValue,**kwargs)
      
    security.declareProtected(permissions.View, 'getResearchProjectInheritedScientificStaffMembers')
    def getResearchProjectInheritedScientificStaffMembers (self, **kwargs):
        """acquire all subprojects' scientific staff members
        """
        atrp_tool = getToolByName(self, 'portal_researchproject')
	lang = self.isTranslatable() and self.getLanguage() or ''
        if self.getResearchProjectInheritScientificStaffMembers():
            raw_staff_members_list = list(self.getField('researchProjectScientificStaffMembers').get(self, **kwargs))
            subproject_objects = atrp_tool.listWfFilteredResearchSubprojects(self, Language=lang)
            for subproject_object in subproject_objects:
                for line in subproject_object.getResearchSubprojectScientificStaffMembers():
                    
                    # this bit of code has to be more versatile, filter multiple staff member names regardless of title etc.
                    # make it a tool method!!!
                    if atrp_tool.structureExtendedLinesField([line], extended_field_format='plain')[0] not in atrp_tool.structureExtendedLinesField(raw_staff_members_list, extended_field_format='plain'):
                        raw_staff_members_list.append(line)
        
        else:
            raw_staff_members_list = self.getField('researchProjectScientificStaffMembers').get(self, **kwargs)
        return atrp_tool.structureExtendedLinesField(raw_staff_members_list,**kwargs)
      
    security.declareProtected(permissions.View, 'getResearchProjectInheritedTechnicalStaffMembers')
    def getResearchProjectInheritedTechnicalStaffMembers (self, **kwargs):
        """acquire all subprojects' technical staff members
        """
        atrp_tool = getToolByName(self, 'portal_researchproject')
	lang = self.isTranslatable() and self.getLanguage() or ''
        if self.getResearchProjectInheritTechnicalStaffMembers():
            raw_staff_members_list = list(self.getField('researchProjectTechnicalStaffMembers').get(self, **kwargs))
            subproject_objects = atrp_tool.listWfFilteredResearchSubprojects(self, Language=lang)
            for subproject_object in subproject_objects:
                for line in subproject_object.getResearchSubprojectTechnicalStaffMembers():
                    
                    # this bit of code has to be more versatile, filter multiple staff member names regardless of title etc.
                    # make it a tool method!!!
                    if atrp_tool.structureExtendedLinesField([line], extended_field_format='plain')[0] not in atrp_tool.structureExtendedLinesField(raw_staff_members_list, extended_field_format='plain'):
                        raw_staff_members_list.append(line)
        
        else:
            raw_staff_members_list = self.getField('researchProjectTechnicalStaffMembers').get(self, **kwargs)
        return atrp_tool.structureExtendedLinesField(raw_staff_members_list,**kwargs)
      
    security.declareProtected(permissions.View, 'getResearchProjectInheritedStudentStaffMembers')
    def getResearchProjectInheritedStudentStaffMembers (self, **kwargs):
        """acquire all subprojects' student staff members
        """
        atrp_tool = getToolByName(self, 'portal_researchproject')
	lang = self.isTranslatable() and self.getLanguage() or ''
        if self.getResearchProjectInheritStudentStaffMembers():
            raw_staff_members_list = list(self.getField('researchProjectStudentStaffMembers').get(self, **kwargs))
            subproject_objects = atrp_tool.listWfFilteredResearchSubprojects(self, Language=lang)
            for subproject_object in subproject_objects:
                for line in subproject_object.getResearchSubprojectStudentStaffMembers():
                    
                    # this bit of code has to be more versatile, filter multiple staff member names regardless of title etc.
                    # make it a tool method!!!
                    if atrp_tool.structureExtendedLinesField([line], extended_field_format='plain')[0] not in atrp_tool.structureExtendedLinesField(raw_staff_members_list, extended_field_format='plain'):
                        raw_staff_members_list.append(line)
        
        else:
            raw_staff_members_list = self.getField('researchProjectStudentStaffMembers').get(self, **kwargs)
        return atrp_tool.structureExtendedLinesField(raw_staff_members_list,**kwargs)
      
    security.declareProtected(permissions.View, 'getResearchProjectInheritedFormerStaffMembers')
    def getResearchProjectInheritedFormerStaffMembers (self, **kwargs):
        """acquire all subprojects' student staff members
        """
        atrp_tool = getToolByName(self, 'portal_researchproject')
	lang = self.isTranslatable() and self.getLanguage() or ''
        if self.getResearchProjectInheritFormerStaffMembers():
            raw_staff_members_list = list(self.getField('researchProjectFormerStaffMembers').get(self, **kwargs))
            subproject_objects = atrp_tool.listWfFilteredResearchSubprojects(self, Language=lang)
            for subproject_object in subproject_objects:
                for line in subproject_object.getResearchSubprojectFormerStaffMembers():
                    
                    # this bit of code has to be more versatile, filter multiple staff member names regardless of title etc.
                    # make it a tool method!!!
                    if atrp_tool.structureExtendedLinesField([line], extended_field_format='plain')[0] not in atrp_tool.structureExtendedLinesField(raw_staff_members_list, extended_field_format='plain'):
                        raw_staff_members_list.append(line)
        
        else:
            raw_staff_members_list = self.getField('researchProjectFormerStaffMembers').get(self, **kwargs)
        return atrp_tool.structureExtendedLinesField(raw_staff_members_list,**kwargs)
      
    security.declareProtected(permissions.View, 'getResearchProjectInheritedFormerStudentStaffMembers')
    def getResearchProjectInheritedFormerStudentStaffMembers (self, **kwargs):
        """acquire all subprojects' student staff members
        """
        atrp_tool = getToolByName(self, 'portal_researchproject')
	lang = self.isTranslatable() and self.getLanguage() or ''
        if self.getResearchProjectInheritFormerStudentStaffMembers():
            raw_staff_members_list = list(self.getField('researchProjectFormerStudentStaffMembers').get(self, **kwargs))
            subproject_objects = atrp_tool.listWfFilteredResearchSubprojects(self, Language=lang)
            for subproject_object in subproject_objects:
                for line in subproject_object.getResearchSubprojectFormerStudentStaffMembers():
                    
                    # this bit of code has to be more versatile, filter multiple staff member names regardless of title etc.
                    # make it a tool method!!!
                    if atrp_tool.structureExtendedLinesField([line], extended_field_format='plain')[0] not in atrp_tool.structureExtendedLinesField(raw_staff_members_list, extended_field_format='plain'):
                        raw_staff_members_list.append(line)
        
        else:
            raw_staff_members_list = self.getField('researchProjectFormerStudentStaffMembers').get(self, **kwargs)
        return atrp_tool.structureExtendedLinesField(raw_staff_members_list,**kwargs)
      
    security.declareProtected(permissions.View, 'getResearchProjectScientificStaffMembers')
    def getResearchProjectScientificStaffMembers (self, **kwargs):
        """we need to wrap this field as the user is allowed to enter extended text infomation
        """
        atrp_tool = getToolByName(self, 'portal_researchproject')
        raw_staff_members_list = self.getField('researchProjectScientificStaffMembers').get(self, **kwargs)
        return atrp_tool.structureExtendedLinesField(raw_staff_members_list,**kwargs)
      
    security.declareProtected(permissions.View, 'getResearchProjectTechnicalStaffMembers')
    def getResearchProjectTechnicalStaffMembers (self, **kwargs):
        """we need to wrap this field as the user is allowed to enter extended text infomation
        """
        atrp_tool = getToolByName(self, 'portal_researchproject')
        raw_staff_members_list = self.getField('researchProjectTechnicalStaffMembers').get(self, **kwargs)
        return atrp_tool.structureExtendedLinesField(raw_staff_members_list,**kwargs)
      
    security.declareProtected(permissions.View, 'getResearchProjectStudentStaffMembers')
    def getResearchProjectStudentStaffMembers (self, **kwargs):
        """we need to wrap this field as the user is allowed to enter extended text infomation
        """
        atrp_tool = getToolByName(self, 'portal_researchproject')
        raw_staff_members_list = self.getField('researchProjectStudentStaffMembers').get(self, **kwargs)
        return atrp_tool.structureExtendedLinesField(raw_staff_members_list,**kwargs)
      
    security.declareProtected(permissions.View, 'getResearchProjectFormerStaffMembers')
    def getResearchProjectFormerStaffMembers (self, **kwargs):
        """we need to wrap this field as the user is allowed to enter extended text infomation
        """
        atrp_tool = getToolByName(self, 'portal_researchproject')
        raw_staff_members_list = self.getField('researchProjectFormerStaffMembers').get(self, **kwargs)
        return atrp_tool.structureExtendedLinesField(raw_staff_members_list,**kwargs)
      
    security.declareProtected(permissions.View, 'getResearchProjectFormerStudentStaffMembers')
    def getResearchProjectFormerStudentStaffMembers (self, **kwargs):
        """we need to wrap this field as the user is allowed to enter extended text infomation
        """
        atrp_tool = getToolByName(self, 'portal_researchproject')
        raw_staff_members_list = self.getField('researchProjectFormerStudentStaffMembers').get(self, **kwargs)
        return atrp_tool.structureExtendedLinesField(raw_staff_members_list,**kwargs)
      
    security.declareProtected(permissions.View, 'getResearchProjectCooperationPartners')
    def getResearchProjectCooperationPartners (self, **kwargs):
      """we need to wrap this field as the user is allowed to enter extended text infomation
      """
      atrp_tool = getToolByName(self, 'portal_researchproject')
      rawFieldValue = self.getField('researchProjectCooperationPartners').get(self, **kwargs)
      return atrp_tool.structureExtendedLinesField(rawFieldValue,**kwargs)
      
    security.declareProtected(permissions.View, 'getResearchProjectContractors')
    def getResearchProjectContractors (self, **kwargs):
      """we need to wrap this field as the user is allowed to enter extended text infomation
      """
      atrp_tool = getToolByName(self, 'portal_researchproject')
      rawFieldValue = self.getField('researchProjectContractors').get(self, **kwargs)
      return atrp_tool.structureExtendedLinesField(rawFieldValue,**kwargs)
      
    security.declareProtected(permissions.View, 'getResearchProjectExternalLinks')
    def getResearchProjectExternalLinks (self, **kwargs):
        """we need to wrap this field as the user is allowed to enter extended text infomation
        """
        atrp_tool = getToolByName(self, 'portal_researchproject')
        raw_external_links = self.getField('researchProjectExternalLinks').get(self, **kwargs)
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
      
    def _addToResearchProjectTree(self, result, data):
        """Adds a piece of content to the result tree."""
        path = data['path']
        parentpath = '/'.join(path.split('/')[:-1])
        # Tell parent about self
        if result.has_key(parentpath):
            result[parentpath]['children'].append(data)
        else:
            result[parentpath] = {'children':[data]}
        # If we have processed a child already, make sure we register it
        # as a child
        if result.has_key(path):
            data['children'] = result[path]['children']
        result[path] = data
															
    security.declareProtected(permissions.View, 'getResearchProjectStructure')
    def getResearchProjectStructure(self, **kwargs):
    
      query = {}
      ctool = getToolByName(self, 'portal_catalog')
      putils = getToolByName(self, 'plone_utils')
      currentPath = '/'.join(self.getPhysicalPath())
      parentPath = '/'.join('/'.join(self.getPhysicalPath()).split('/')[:-1])
      query['path'] = {'query': parentPath,
                       'depth': 1000,
		      }
      query['sort_on'] = 'getObjPositionInParent'	      
      #query['portal_type'] = ('ResearchProject', 'ResearchSubproject','ResearchProjectInternalFolder','BibliographyList','BibliographyTopic',)
      
      rawresult = ctool(**query)
      
      result = {}
      for item in [ rawitem for rawitem in rawresult if rawitem.getPath().startswith(currentPath) ]:
        path = item.getPath()
        item_url = item.getURL()
        data = {
	    'path' : path,
	    'Title': putils.pretty_title_or_id(item),
	    'icon': item.getIcon,
	    'absolute_url': item_url,
	    'portal_type': item.portal_type,
	    'review_state': item.review_state,
	    'Description': item.Description,
	    'children': [],
	}
	self._addToResearchProjectTree(result, data)
	
      if result.has_key(currentPath):
        return result[currentPath]
      else:
        return {}
      
    security.declareProtected(permissions.View, 'getLogoTag')
    def getLogoTag(self, **kwargs):
        """
        Generate logo image tag using the api of the ImageField
        """
        return self.getField('logo').tag(self, **kwargs)
			
    security.declareProtected(permissions.View, 'getAvailableLogoSizes')
    def getAvailableLogoSizes(self, **kwargs):
        """
        Generate logo image tag using the api of the ImageField
        """
        return self.getField('logo').getAvailableSizes(self, **kwargs)
									    
    security.declareProtected(permissions.View, 'hasResearchSubprojects')
    def hasResearchSubprojects(self, **kwargs):
        """
        Be True if research project has subprojects
        """
	filter_wf_states = kwargs.get('filter_wf_states', False)
	atrp_tool = getToolByName(self, 'portal_researchproject')

	if filter_wf_states and atrp_tool.listWfFilteredResearchSubprojects(self):
	    return True
	elif atrp_tool.listResearchSubprojects(self):
	    return True

	return False	    
			
    security.declareProtected(permissions.View, 'listResearchSubprojects')
    def listResearchSubprojects(self, **kwargs):
        """
        Return subprojects if any
        """
	filter_wf_states = kwargs.get('filter_wf_states', False)
	atrp_tool = getToolByName(self, 'portal_researchproject')

	if self.hasResearchSubprojects(**kwargs):

	    if filter_wf_states:
		return atrp_tool.listWfFilteredResearchSubprojects(self)
	    else:
		return atrp_tool.listResearchSubprojects(self)
	    
	return ()
			
    security.declareProtected(permissions.View, 'getResearchProjectObject')
    def getResearchProjectObject(self, **kwargs):
        """
        Make the object instance of a research project known to the project's subproject children without much hassle...
        """
	obj = self
	while 1:
	  if obj.portal_type == 'ResearchProject':
	    break
	  else: 
	    obj = obj.aq_inner.aq_parent
	
	return obj    
			
    security.declareProtected(permissions.View, 'getResearchProjectUrl')
    def getResearchProjectUrl(self, **kwargs):
        """
        Make the URL of a research project known to the project's subproject children without much hassle...
        """
	return self.getResearchProjectObject().absolute_url(**kwargs)    
			
    security.declareProtected(permissions.View, 'getResearchProjectInvolvedDepartmentsLongname')
    def getResearchProjectInvolvedDepartmentsLongname(self, **kwargs):
        """
        Get the long name of the department from the research project site configuration tool
        """
        involvedDepartmentIDs = self.getResearchProjectInvolvedDepartments()
	if hasattr (self, ATRP_TOOL_ID):
	  
	  atrp_tool = getToolByName(self, ATRP_TOOL_ID)
  	  involvedDepartmentLongnames = []
	  
	  for id in involvedDepartmentIDs:
	    involvedDepartmentLongnames.append(atrp_tool.getDepartmentLongnameById(id))
	    
	  return involvedDepartmentLongnames
	
	else:    
	  return departmentIDs

    def at_post_create_script(self):
        """ tending subproject info fields of LinguaPlone objects
        """
        self.reindexTranslationObjects()
	OrderedBaseFolder.at_post_create_script(self)
            							    	
    def at_post_edit_script(self):
        """ tending subproject info fields of LinguaPlone objects
        """
        self.reindexTranslationObjects()
	OrderedBaseFolder.at_post_edit_script(self)
            							    	
    def __bobo_traverse__(self, REQUEST, name):
        """
        Transparent access to logo image scales
        """
        if name.startswith('logo'):
            field = self.getField('logo')
            logo = None
            if name == 'logo':
                logo = field.getScale(self)
            else:
                scalename = name[len('logo_'):]
                if scalename in self.getAvailableLogoSizes().keys():
	          logo = field.getScale(self, scale=scalename)
	    if logo is not None and not isinstance(logo, basestring):
	      return logo
        
	return OrderedBaseFolder.__bobo_traverse__(self, REQUEST, name)
																																				  
#    def allowedContentTypes(self):
#        """
#        restrict allowed content types to a dedicated list of ctypes
#        """
#	all_allowed_ctypes = [ ctype for ctype in OrderedBaseFolder.allowedContentTypes(self) ]
#        atrp_tool = getToolByName (self, ATRP_TOOL_ID)
#	print atrp_tool.allowed_content_types_researchproject
#	return [ ctype for ctype in all_allowed_ctypes if ctype.getId() in atrp_tool.allowed_content_types_researchproject ]

registerType(ResearchProject,PROJECTNAME)
