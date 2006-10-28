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
"""ResearchProjectTool main class"""

# Python stuff
import re, string

try: 
  from Products.LinguaPlone.public import DisplayList
except:
  # multilingual support
  from Products.Archetypes.public import DisplayList
  
# Zope stuff
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
import AccessControl.Owned
from OFS.SimpleItem import SimpleItem
from OFS.PropertyManager import PropertyManager
from ZODB.PersistentList import PersistentList
from Products.CMFCore.Expression import Expression
from Products.CMFCore.permissions import View, ManagePortal
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.utils import UniqueObject
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from Products.ATResearchProject.config import ATRP_DIR
from Products.ATResearchProject.config import WWW_DIR
from Products.ATResearchProject.config import PROJECTNAME
from Products.ATResearchProject.config import ATRP_TOOL_ID
from Products.ATResearchProject.config import ATRP_TOOL_NAME
from Products.ATResearchProject.config import PROJECTLIST_CRITERIAFIELDS
from Products.ATResearchProject.config import PROJECTLIST_SORTFIELDS


from Products.ATContentTypes.tool.topic import TopicIndex
view_permission = ManagePortal

class ResearchProjectSiteConfiguration(UniqueObject, SimpleItem, PropertyManager):
    """Tool for managing site-wide research project variables
       as well as some resources of the ResearchProject and Subproject
       entries.
    """

    id = ATRP_TOOL_ID
    meta_type = ATRP_TOOL_NAME
    title = ATRP_TOOL_NAME
    plone_tool = True
    
    __implements__ = (SimpleItem.__implements__,)
    
    security = ClassSecurityInfo()
    infoPage = PageTemplateFile(WWW_DIR + '/research_project_tool_zmi.pt', globals())
    security.declareProtected(view_permission, 'infoPage')

    manage_options = (
        ({'label':'Information', 'action':'infoPage'},
        SimpleItem.manage_options[0])
	+ PropertyManager.manage_options
	+ AccessControl.Owned.Owned.manage_options
	+ SimpleItem.manage_options[2:]
        )

    _properties = PropertyManager._properties + (
        {'id':'department_ids',
         'type':'lines',
         'mode':'w',
         },
        {'id':'department_urls',
         'type':'lines',
         'mode':'w',
         },
        {'id':'department_names',
         'type':'lines',
         'mode':'w',
         },
        )


    def __init__(self):
        self.department_ids = PersistentList()
        self.department_urls = PersistentList()
        self.department_names = PersistentList()

	self.rplist_indexes =  {}
        # initializing criteria indexes for research project lists    
        for crit_field in PROJECTLIST_CRITERIAFIELDS + PROJECTLIST_SORTFIELDS:
    	    index = {}
    	    index_name = crit_field['field'][0]
    	    index['friendlyName'] = crit_field['field'][1]
    	    index['description'] = crit_field['field'][2]
    	    index['criteria'] = crit_field['ctypes']
	    indexObj = TopicIndex(index_name, **index)

	    self.rplist_indexes[index_name] = indexObj


    def getAuthorsLine (self, atrp_object, **kwargs):
        """render a structural line for the authors line in project headers
        """
        authorsline = ''
        if atrp_object.getAuthors(**kwargs):
            authorsline = atrp_object.getAuthors(**kwargs)[0]
        if len (atrp_object.getAuthors(**kwargs)) > 1:
            for author in atrp_object.getAuthors(**kwargs)[1:]:
                authorsline = '%s, %s' % (authorsline, author)
                                                            
        return authorsline
                                                                                                

    def getRPListCriteriaIndex(self, index_name):
    
	if self.rplist_indexes.has_key(index_name):
	    return self.rplist_indexes[index_name]
	else:
	    raise AttributeError ('Index ' + str(index_name) + ' not found')

    def structureExtendedLinesField(self, lines_field, **kwargs):
      """ parses the lines in the LinesField and searches for tags that add hyperref information to the 
      field text"""
      
      extendedLinesField = []
    
      # detect the output format for the lines in the LinesField 
      if kwargs.get('extended_field_format', False):
        formatType = kwargs.get('extended_field_format')
      else:
        formatType = 'raw'
    
      # go through each line
      for line in lines_field:
      
        # a tag is a phrase enclosed by "<>". No blanks are allowed between the brackets
        text = string.rstrip(' '.join([ word for word in string.split(line, ' ') if word[0]+word[len(word)-1] != '<>' ]))
        tag = string.rstrip(' '.join([ word for word in string.split(line, ' ') if word[0]+word[len(word)-1] == '<>' ]))
        
	# we have three format types: 
	#   o plain: no hyperrefs, strip the tags of the line
	#   o structure: tags define hyperrefs for each line
	#   o raw: do nothing, return the entire line as it is
        if formatType == 'plain':
        
	  extendedLinesField.append(text)
        
	elif formatType == 'structure':
        
	  extended_field_structure = text
          # ignore tags for this line if more than one tag is specified for this line
          if len(string.split(tag,' ')) == 1:
	    
	    tagType = string.split(tag,':')[0][1:]
	    tagContent = ':'.join(string.split(tag,':')[1:])[:-1]
	    if (tagType == 'member') or (tagType == 'uid'):

              # see, if the specified memberUid exists on this site and, if so, hyperlink the text to the member's home page
	      memberUid = tagContent
	      mtool = getToolByName(self, 'portal_membership')

	      #if just the tag is given try to get the fullname
              if not text:
                member = mtool.getMemberById(memberUid)
                if member:
                    
                    if member.hasProperty('academic_title') and (member.getPropertyType('academic_title') == 'string') and member.getProperty('academic_title'):
                        text = string.strip(member.getProperty('academic_title') + ' ' + member.getProperty('fullname'))
                    elif member.hasProperty('academictitle') and (member.getPropertyType('academictitle') == 'string') and member.getProperty('academictitle'):
                        text = string.strip(member.getProperty('academictitle') + ' ' + member.getProperty('fullname'))
                    elif member.hasProperty('academic_title') and (member.getPropertyType('academic_title') == 'lines') and member.getProperty('academic_title'):
                        text = string.strip(member.getProperty('academic_title')[0] + ' ' + member.getProperty('fullname'))
			try:
			    text = string.strip(text + ' ' + member.getProperty('academic_title')[1])
			except IndexError:
			    pass   
                    elif member.hasProperty('academictitle') and (member.getPropertyType('academictitle') == 'lines') and member.getProperty('academictitle'):
                        
			text = string.strip(member.getProperty('academictitle')[0] + ' ' + member.getProperty('fullname'))
			try:
			    text = string.strip(text + ' ' + member.getProperty('academictitle')[1])
			except IndexError:
			    pass    
                    else:
                        text = member.getProperty('fullname')
		              
	      # override if home page exists
              if mtool.getHomeUrl(memberUid):
                extended_field_structure = '<a href="%s">%s</a>' % (mtool.getHomeUrl(memberUid), text)
	      else:
	        extended_field_structure = text

 	    elif tagType == 'url':
	     
	      url = tagContent
	      if url:
                extended_field_structure = '<a href="%s" target="_new">%s</a>' % (url, text) 
	    
	    elif tagType == 'mailto':

	      mailAddress = tagContent
	      if '@' in mailAddress:
                extended_field_structure = '<a href="&#0109;ailto&#0058;' + mailAddress.replace('@', '&#0064;').replace(':', '&#0058;') + '">' + text + '</a>'

          if extended_field_structure:
              extendedLinesField.append(extended_field_structure)
        
	else:
        
	  extendedLinesField.append(line)

      return extendedLinesField

    def getDepartmentLongnameById(self, short_name):
      
      departmentIDs = list(self.department_ids)
      departmentNames = self.department_names

      if hasattr(self, 'portal_languages'):
        lang_tool = getToolByName (self, 'portal_languages')
        lang = lang_tool.getPreferredLanguage()
	if self.getProperty('department_names-%s' % lang):
	  departmentNames = self.getProperty('department_names-%s' % lang)
      
      idPos = departmentIDs.index(short_name)
      
      try:
        return departmentNames[idPos]
      except IndexError:
        return departmentIDs[idPos]
	  
    def getDepartmentUrlById(self, short_name):
      
      departmentIDs = list(self.department_ids)
      departmentURLs = self.department_urls

      if hasattr(self, 'portal_languages'):
        lang_tool = getToolByName (self, 'portal_languages')
        lang = lang_tool.getPreferredLanguage()
	if self.getProperty('department_urls-%s' % lang):
	  departmentURLs = self.getProperty('department_urls-%s' % lang)
      
      idPos = departmentIDs.index(short_name)
      
      try:
        return departmentURLs[idPos]
      except IndexError:
        return ''
	  
    def getDepartmentDisplayList(self):
      
      departmentIDs = self.department_ids
      departmentNames = self.department_names

      if hasattr(self, 'portal_languages'):
        lang_tool = getToolByName (self, 'portal_languages')
        lang = lang_tool.getPreferredLanguage()
	if self.getProperty('department_names-%s' % lang):
	  departmentNames = self.getProperty('department_names-%s' % lang)
      
      departmentDisplayList = []
      for idPos in range(len(departmentIDs)):
        try:
          douple = (departmentIDs[idPos], departmentNames[idPos])
	except IndexError:
	  douple = (departmentIDs[idPos], departmentIDs[idPos])
	  
	departmentDisplayList.append(douple)
		
      return DisplayList(departmentDisplayList)
	
    def getDepartmentSelectionList(self):
      
      departmentIDs = self.department_ids
      departmentNames = self.department_names

      if hasattr(self, 'portal_languages'):
        lang_tool = getToolByName (self, 'portal_languages')
        lang = lang_tool.getPreferredLanguage()
	if self.getProperty('department_names-%s' % lang):
	  departmentNames = self.getProperty('department_names-%s' % lang)
      
      departmentSelectionList = []
      for idPos in range(len(departmentIDs)):
        try:
          douple = (departmentIDs[idPos], '%s (%s)' % (departmentIDs[idPos], departmentNames[idPos]))
	except IndexError:
	  douple = (departmentIDs[idPos], departmentIDs[idPos])
	  
	departmentSelectionList.append(douple)
		
      return DisplayList(departmentSelectionList)
	
    def hasResearchProjects(self):
      
      if self.listResearchProjects():
        return True		

      return False

    def hasResearchSubprojects(self, project_object):
      
      if self.listResearchSubprojects(project_objects):
        return True		

      return False

    def hasResearchFields(self):
      
      if self.listResearchFields():
        return True		

      return False

    def listResearchProjects(self, sort_on='', sort_order=''):
      
      query = {}
      ctool = getToolByName(self, 'portal_catalog')
      ntp = getToolByName(self, 'portal_properties').navtree_properties
      utool = getToolByName(self, 'portal_url')
      portal = utool.getPortalObject()
      portalPath = '/'.join(portal.getPhysicalPath())
      query['path'] = {'query': portalPath,
                       'depth': 1000,
                       }
      query['portal_type'] = ('ResearchProject')
      if sort_on:
        query['sort_on'] = sort_on
      if sort_order:
         query['sort_order'] = sort_order
      rawresult = ctool(**query)
		
      return rawresult
      
    def listWfFilteredResearchProjects(self, sort_on='', sort_order=''):
      
      query = {}
      ctool = getToolByName(self, 'portal_catalog')
      ntp = getToolByName(self, 'portal_properties').navtree_properties
      utool = getToolByName(self, 'portal_url')
      portal = utool.getPortalObject()
      portalPath = '/'.join(portal.getPhysicalPath())
      query['path'] = {'query': portalPath,
                       'depth': 1000,
                       }
      query['portal_type'] = ('ResearchProject')
      if ntp.getProperty('enable_wf_state_filtering', False):
         query['review_state'] = ntp.wf_states_to_show
      if sort_on:
         query['sort_on'] = sort_on
      if sort_order:
         query['sort_order'] = sort_order
      rawresult = ctool(**query)
		
      return rawresult
      
    def listResearchFields(self):
      
      query = {}
      ctool = getToolByName(self, 'portal_catalog')
      ntp = getToolByName(self, 'portal_properties').navtree_properties
      utool = getToolByName(self, 'portal_url')
      portal = utool.getPortalObject()
      portalPath = '/'.join(portal.getPhysicalPath())
      query['path'] = {'query': portalPath,
                       'depth': 1000,
                       }
      query['portal_type'] = ('ResearchField')
      #if ntp.getProperty('enable_wf_state_filtering', False):
      #   query['review_state'] = ntp.wf_states_to_show
      rawresult = ctool(**query)
		
      return rawresult	

    def listWfFilteredResearchFields(self):
      
      query = {}
      ctool = getToolByName(self, 'portal_catalog')
      ntp = getToolByName(self, 'portal_properties').navtree_properties
      utool = getToolByName(self, 'portal_url')
      portal = utool.getPortalObject()
      portalPath = '/'.join(portal.getPhysicalPath())
      query['path'] = {'query': portalPath,
                       'depth': 1000,
                       }
      query['portal_type'] = ('ResearchField')
      if ntp.getProperty('enable_wf_state_filtering', False):
         query['review_state'] = ntp.wf_states_to_show
      rawresult = ctool(**query)
		
      return rawresult	

    def getResearchFieldsDisplayList(self):
      
      putils = getToolByName(self, 'plone_utils')
      researchFieldDisplayList = []
      for topic in self.listResearchFields():
        path = topic.getPath()
	title = putils.pretty_title_or_id(topic)
	description = topic.getObject().getDescription()
	researchFieldDisplayList.append((path, '%s (%s)' % (title, description)))
	
      return DisplayList(researchFieldDisplayList)	

    def getResearchProjectsListForField(self, topic, sort_on='', sort_order=''):

      researchProjectList = []
      listOfAllResearchProjects = self.listResearchProjects(sort_on=sort_on, sort_order=sort_order)
      if listOfAllResearchProjects:
        for rp in listOfAllResearchProjects:
          if topic in rp.getObject().getResearchProjectResearchFields():
	    researchProjectList.append(rp.getObject())
	
      return researchProjectList

    def getWfFilteredResearchProjectsListForField(self, field, sort_on='', sort_order=''):

      researchProjectList = []
      listOfAllResearchProjects = self.listWfFilteredResearchProjects(sort_on=sort_on, sort_order=sort_order)
      if listOfAllResearchProjects:
        for rp in listOfAllResearchProjects:
          if field in rp.getObject().getResearchProjectResearchFields():
	    researchProjectList.append(rp.getObject())
	
      return researchProjectList

    def listResearchSubprojects(self, rp_object=None):
      
      query = {}
      subproject_objects = []
      
      if not rp_object:
        utool = getToolByName(self, 'portal_url')
        portal = utool.getPortalObject()
        portalPath = '/'.join(portal.getPhysicalPath())
        query_path = portalPath
      else:
        rp_path = '/'.join(rp_object.getPhysicalPath())
        query_path = rp_path
            
      ctool = getToolByName(self, 'portal_catalog')
      #ntp = getToolByName(self, 'portal_properties').navtree_properties
      query['path'] = {'query': query_path,
                       'depth': 1000,
                       }
      query['portal_type'] = ('ResearchSubproject')
      #if ntp.getProperty('enable_wf_state_filtering', False):
      #   query['review_state'] = ntp.wf_states_to_show
      rawresult = ctool(**query)
      
      for brain_obj in rawresult:
        subproject_objects.append(brain_obj.getObject())

      return subproject_objects	

    def siteHasResearchFields(self):
    
	ctool = getToolByName(self, 'portal_catalog')
	return ctool(portal_type=('ResearchField',)) and True or False

    def listWfFilteredResearchSubprojects(self, rp_object=None):
      
      query = {}
      subproject_objects = []
      
      if not rp_object:
        utool = getToolByName(self, 'portal_url')
        portal = utool.getPortalObject()
        portalPath = '/'.join(portal.getPhysicalPath())
        query_path = portalPath
      else:
        rp_path = '/'.join(rp_object.getPhysicalPath())
        query_path = rp_path
            
      ctool = getToolByName(self, 'portal_catalog')
      ntp = getToolByName(self, 'portal_properties').navtree_properties
      query['path'] = {'query': query_path,
                       'depth': 1000,
                       }
      query['portal_type'] = ('ResearchSubproject')
      if ntp.getProperty('enable_wf_state_filtering', False):
         query['review_state'] = ntp.wf_states_to_show
      rawresult = ctool(**query)
      
      for brain_obj in rawresult:
        subproject_objects.append(brain_obj.getObject())

      return subproject_objects	

InitializeClass(ResearchProjectSiteConfiguration)
