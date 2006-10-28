import os
from Products.CMFCore.permissions import AddPortalContent
from ZPublisher.HTTPRequest import record

ADD_CONTENT_PERMISSION = AddPortalContent
PROJECTNAME = "ATResearchProject"
SKINS_DIR = 'skins'

GLOBALS = globals()
ATRP_DIR = os.path.abspath(os.path.dirname(__file__))
WWW_DIR = os.path.join(ATRP_DIR, 'www')
ATRP_TOOL_ID = 'portal_researchproject'
ATRP_TOOL_NAME = 'Research Project Site Configuration'
INFINITY = '2039/12/31'

PROJECT_INFOFIELD_ACCESSORS = [
    'getResearchProjectProjectCoordinators', 
    'getResearchProjectScientificCoordinators',
    'getResearchProjectContactPersons',
    'getResearchProjectInheritedScientificStaffMembers',
    'getResearchProjectInheritedTechnicalStaffMembers',
    'getResearchProjectInheritedStudentStaffMembers',
    'getResearchProjectInheritedFormerStaffMembers',
    'getResearchProjectInheritedFormerStudentStaffMembers',
    'getResearchProjectCooperationPartners',
    'getResearchProjectContractors',
]
SUBPROJECT_INFOFIELD_ACCESSORS = [
    'getResearchSubprojectScientificCoordinators',
    'getResearchSubprojectInheritedScientificStaffMembers',
    'getResearchSubprojectInheritedTechnicalStaffMembers',
    'getResearchSubprojectInheritedStudentStaffMembers',
    'getResearchSubprojectInheritedFormerStaffMembers',
    'getResearchSubprojectInheritedFormerStudentStaffMembers',
    'getResearchSubprojectCooperationPartners',
]

atrp_extended_fieldstructure_tags = ('member','uid','url','mailto')

# do not touch this variable structure!!! unless you know what you are doing!!! actually do not touch anything in this file, 
# use myConfig.py instead!!!
try:
    import Products.TextIndexNG2
    # extra args for the TextIndexNG2 index to be added to portal_catalog
    ting2_extra = record()
    ting2_extra.indexed_fields   = ''
    ting2_extra.default_encoding = 'utf-8'
    ting2_extra.use_converters   = 1
    text_index_type = {'type': 'TextIndexNG2', 'extra': ting2_extra, }
except ImportError:
    # do not at all touch zcti_extra, it is needed to created ZCTextIndex catalog indexes
    zcti_extra = record()
    zcti_extra.lexicon_id = 'plone_lexicon'
    zcti_extra.index_type = 'Okapi BM25 Rank'
    zcti_extra.doc_attr   = None
    text_index_type = {'type': 'ZCTextIndex', 'extra': zcti_extra, }
    
PROJECTLIST_CRITERIAFIELDS = [
    {
	'portal_type'	: 'ResearchProject',
	'field'		: ('searchableResearchProjectText', 'Search all Research Project Text Fields',
			   'This criterion looks at all searchable text passages in research project objects.',),
        'index_type'    : text_index_type,
	'ctypes'	: ('ATSimpleStringCriterion', )
    },	
    {
	'portal_type'	: 'ResearchProject',
	'field'		: ('getResearchProjectInfoFields', 'Search all Research Project Info Fields',
			   'This criterion looks at all information fields in research project objects.',),
        'index_type'    : text_index_type,
	'ctypes'	: ('ATSimpleStringCriterion', )
    },	
    {
	'portal_type'	: 'ResearchProject',
	'field'		: ('researchProjectRuntimeStart','Start of Research Project\'s runtime',''),
        'index_type'    : { 'type': 'DateIndex', },
	'ctypes'	: ('ATDateRangeCriterion', 'ATFriendlyDateCriteria',)
    },	
    {
	'portal_type'	: 'ResearchProject',
	'field'		: ('researchProjectRuntimeEnd','End of Research Project\'s runtime',''),
        'index_type'    : { 'type': 'DateIndex', },
	'ctypes'	: ('ATDateRangeCriterion', 'ATFriendlyDateCriteria', )
    },	
    {
	'portal_type'	: 'ResearchProject',
	'field'		: ('researchProjectKeywords', 'Research Project - Keywords','',),
        'index_type'    : text_index_type,
	'ctypes'	: ('ATSimpleStringCriterion', )
    },
    {
	'portal_type'	: 'ResearchProject',
	'field'		: ('researchProjectProjectCoordinators', 'Research Project - Project Coordinator', '',),
        'index_type'    : text_index_type,
	'ctypes'	: ('ATSimpleStringCriterion', )
    },	
    {
	'portal_type'	: 'ResearchProject',
	'field'		: ('researchProjectScientificCoordinators', 'Research Project - Scientific Coordinator','',),
        'index_type'    : text_index_type,
	'ctypes'	: ('ATSimpleStringCriterion', )
    },
    {
	'portal_type'	: 'ResearchProject',
	'field'		: ('researchProjectContactPersons', 'Research Project - Contact Person', '',),
        'index_type'    : text_index_type,
	'ctypes'	: ('ATSimpleStringCriterion', )
    },	
    {	
	'portal_type'	: 'ResearchProject',
	'field'		: ('researchProjectInvolvedDepartments', 'Research Project - Involved Department', '',),
        'index_type'    : text_index_type,
	'ctypes'	: ('ATSimpleStringCriterion', )
    },
    {	
	'portal_type'	: 'ResearchProject',
	'field'		: ('researchProjectScientificStaffMembers', 'Research Project - Scientific Staff Member','',),
        'index_type'    : text_index_type,
	'ctypes'	: ('ATSimpleStringCriterion', )
    },	
    {	
	'portal_type'	: 'ResearchProject',
	'field'		: ('researchProjectTechnicalStaffMembers','Research Project - Technical Staff Member',''),
        'index_type'    : text_index_type,
	'ctypes'	: ('ATSimpleStringCriterion', )
    },
    {	
	'portal_type'	: 'ResearchProject',
	'field'		: ('researchProjectStudentStaffMembers', 'Research Project - Student Staff Member','',),
        'index_type'    : text_index_type,
	'ctypes'	: ('ATSimpleStringCriterion', )
    },	
    {	
	'portal_type'	: 'ResearchProject',
	'field'		: ('researchProjectFormerStaffMembers','Research Project - Former Staff Member',''),
        'index_type'    : text_index_type,
	'ctypes'	: ('ATSimpleStringCriterion', )
    },
    {	
	'portal_type'	: 'ResearchProject',
	'field'		: ('researchProjectFormerStudentStaffMembers', 'Research Project - Former Student Staff Member','',),
        'index_type'    : text_index_type,
	'ctypes'	: ('ATSimpleStringCriterion', )
    },	
    {
	'portal_type'	: 'ResearchProject',
	'field'		: ('researchProjectCooperationPartners', 'Research Project - Cooperation Partner','',),
        'index_type'    : text_index_type,
	'ctypes'	: ('ATSimpleStringCriterion', )
    },
    {	
	'portal_type'	: 'ResearchProject',
	'field'		: ('researchProjectContractors', 'Research Project - Contractor','',),
        'index_type'    : text_index_type,
	'ctypes'	: ('ATSimpleStringCriterion', )
    },
    {	
	'portal_type'	: 'ResearchProject',
	'field'		: ('researchProjectThirdPartyFunded', 'Research Project - Third-party funded','',),
        'index_type'    : { 'type': 'FieldIndex', },
	'ctypes'	: ('ATBooleanCriterion', )
    },
    {	
	'portal_type'	: 'ResearchProject',
	'field'		: ('pathResearchProject','Research Project - Website Path',
	                   'This criterion allows it to restrict query results for research projects to the selected website paths.'),
        'index_type'    : { 'type': 'ExtendedPathIndex', },
	'ctypes'	: ('ATPathCriterion',)
    },
    {
	'portal_type'	: 'ResearchSubproject',
	'field'		: ('searchableResearchSubprojectText', 'Search all Research Subproject Text Fields',
			   'This criterion looks at all searchable text passages in research subproject objects.',),
        'index_type'    : text_index_type,
	'ctypes'	: ('ATSimpleStringCriterion', )
    },	
    {
	'portal_type'	: 'ResearchSubproject',
	'field'		: ('getResearchSubprojectInfoFields', 'Search all Research Subproject Info Fields',
			   'This criterion looks at all information fields in research subproject objects.',),
        'index_type'    : text_index_type,
	'ctypes'	: ('ATSimpleStringCriterion', )
    },	
    {
	'portal_type'	: 'ResearchSubproject',
	'field'		: ('researchSubprojectRuntimeStart','Start of Research Subproject\'s runtime',''),
        'index_type'    : { 'type': 'DateIndex', },
	'ctypes'	: ('ATDateRangeCriterion', 'ATFriendlyDateCriteria',)
    },	
    {
	'portal_type'	: 'ResearchSubproject',
	'field'		: ('researchSubprojectRuntimeEnd','End of Research Subproject\'s runtime',''),
        'index_type'    : { 'type': 'DateIndex', },
	'ctypes'	: ('ATDateRangeCriterion', 'ATFriendlyDateCriteria',)
    },	
    {
	'portal_type'	: 'ResearchSubproject',
	'field'		: ('researchSubprojectKeywords', 'Research Subproject - Keywords','',),
        'index_type'    : text_index_type,
	'ctypes'	: ('ATSimpleStringCriterion', )
    },
    {	
	'portal_type'	: 'ResearchSubproject',
	'field'		: ('researchSubprojectScientificCoordinators','Research Subproject - Scientific Coordinator',''),
        'index_type'    : text_index_type,
	'ctypes'	: ('ATSimpleStringCriterion', )
    },
    {	
	'portal_type'	: 'ResearchSubproject',
	'field'		:('researchSubprojectInvolvedDepartments','Research Subproject - Involved Department',''),
        'index_type'    : text_index_type,
	'ctypes'	: ('ATSimpleStringCriterion', )
    },
    {	
	'portal_type'	: 'ResearchSubproject',
	'field'		: ('researchSubprojectScientificStaffMembers','Research Subproject - Scientific Staff Member',''),
        'index_type'    : text_index_type,
	'ctypes'	: ('ATSimpleStringCriterion', )
    },
    {	
	'portal_type'	: 'ResearchSubproject',
	'field'		: ('researchSubprojectTechnicalStaffMembers','Research Subproject - Technical Staff Member',''),
        'index_type'    : text_index_type,
	'ctypes'	: ('ATSimpleStringCriterion', )
    },
    {	
	'portal_type'	: 'ResearchSubproject',
	'field'		: ('researchSubprojectStudentStaffMembers','Research Subproject - Student Staff Member',''),
        'index_type'    : text_index_type,
	'ctypes'	: ('ATSimpleStringCriterion', )
    },
    {	
	'portal_type'	: 'ResearchSubproject',
	'field'		: ('researchSubprojectFormerStaffMembers','Research Subproject - Former Staff Member',''),
        'index_type'    : text_index_type,
	'ctypes'	: ('ATSimpleStringCriterion', )
    },
    {	
	'portal_type'	: 'ResearchSubproject',
	'field'		: ('researchSubprojectFormerStudentStaffMembers','Research Subproject - Former Student Staff Member',''),
        'index_type'    : text_index_type,
	'ctypes'	: ('ATSimpleStringCriterion', )
    },
    {	
	'portal_type'	: 'ResearchSubproject',
	'field'		: ('researchSubprojectExternalInstitutes','Research Subproject - External Institute',''),
        'index_type'    : text_index_type,
	'ctypes'	: ('ATSimpleStringCriterion', )
    },
    {	
	'portal_type'	: 'ResearchSubproject',
	'field'		: ('researchSubprojectCooperationPartners','Research Subproject - Cooperation Partner',''),
        'index_type'    : text_index_type,
	'ctypes'	: ('ATSimpleStringCriterion', )
    },
    {	
	'portal_type'	: 'ResearchSubproject',
	'field'		: ('pathResearchSubproject','Research Subproject - Website Path',
	                   'This criterion allows it to restrict query results for research subprojects to the selected website paths.'),
        'index_type'    : { 'type': 'ExtendedPathIndex', },
	'ctypes'	: ('ATPathCriterion',)
    },
]
PROJECTLIST_SORTFIELDS = [
    {
	'portal_type'	: 'ResearchProject',
	'field'		: ('researchProjectRuntimeStart','Start of Research Project\'s runtime',''),
        'index_type'    : { 'type': 'DateIndex', },
	'ctypes'	: ('ATSortCriterion', 'ATDateRangeCriterion', 'ATFriendlyDateCriteria',)
    },	
    {
	'portal_type'	: 'ResearchProject',
	'field'		: ('researchProjectRuntimeEnd','End of Research Project\'s runtime',''),
        'index_type'    : { 'type': 'DateIndex', },
	'ctypes'	: ('ATSortCriterion', 'ATDateRangeCriterion', 'ATFriendlyDateCriteria',)
    },	
    {
	'portal_type'	: 'ResearchProject',
	'field'		: ('titleResearchProject','Research Project - Title',''),
        'index_type'    : { 'type': 'FieldIndex', },
	'ctypes'	: ('ATSortCriterion',)
    },	
    {
	'portal_type'	: 'ResearchProject',
	'field'		: ('researchProjectOfficialTitle','Research Project - Official Title',''),
        'index_type'    : { 'type': 'FieldIndex', },
	'ctypes'	: ('ATSortCriterion',)
    },	
    {
	'portal_type'	: 'ResearchSubproject',
	'field'		: ('researchSubprojectRuntimeStart','Start of Research Subproject\'s runtime',''),
        'index_type'    : { 'type': 'DateIndex', },
	'ctypes'	: ('ATSortCriterion', 'ATDateRangeCriterion', 'ATFriendlyDateCriteria',)
    },	
    {
	'portal_type'	: 'ResearchSubproject',
	'field'		: ('researchSubprojectRuntimeEnd','End of Research Subproject\'s runtime',''),
        'index_type'    : { 'type': 'DateIndex', },
	'ctypes'	: ('ATSortCriterion', 'ATDateRangeCriterion', 'ATFriendlyDateCriteria',)
    },	
    {
	'portal_type'	: 'ResearchSubproject',
	'field'		: ('titleResearchSubproject','Research Subproject - Title',''),
        'index_type'    : { 'type': 'FieldIndex', },
	'ctypes'	: ('ATSortCriterion',)
    },	
    {
	'portal_type'	: 'ResearchSubproject',
	'field'		: ('researchSubprojectOfficialTitle','Research Subproject - Official Title',''),
        'index_type'    : { 'type': 'FieldIndex', },
	'ctypes'	: ('ATSortCriterion',)
    },	
]


# generated from the PROJECTLIST_CRITERIAFIELDS
CATALOG_INDEXES = [ dict([('name',criterion['field'][0])] + [ (key, criterion['index_type'][key]) for key in criterion['index_type'].keys() ])  for criterion in (PROJECTLIST_CRITERIAFIELDS + PROJECTLIST_SORTFIELDS) if criterion['field'][0].startswith('research') or criterion['field'][0].startswith('getResearch')]
CATALOG_METADATA = [ criterion['field'][0] for criterion in PROJECTLIST_SORTFIELDS if criterion['field'][0].startswith('research') or criterion['field'][0].startswith('getResearch') ]
DEPRECATED_CATALOG_INDEXES = [ 'researchProjectInfoFields', 'researchSubprojectInfoFields',]
DEPRECATED_CATALOG_METADATA = []
try:
  from myConfig import DEPARTMENT_DEFAULTS
except:
  DEPARTMENT_DEFAULTS = {'department_ids': ['UNCONFIGURED'],'department_urls': [],'department_names': ['Not configured yet, visit portal control panel!'],}

try:
  from myConfig import ALLOWED_CT_DEFAULTS
except:
  ALLOWED_CT_DEFAULTS = {
    'allowed_content_types_researchproject': (
            'ResearchSubproject',
            'Document',
            'Image',
            'ResearchProjectInternalFolder',
            'ResearchProjectList',
            'File',
            'PhotoAlbum',
            'BibliographyFolder',
            'BibliographyList',
	    'BibliographyTopic',
            'ATPhotoAlbum',
	    'Ploneboard',
	    'Link',
	    'File',
	    'Topic',
	    'MemberInfo',
	    'MemberList',
    ),
    'allowed_content_types_subproject': (
            'ResearchSubproject',
            'Document',
            'Image',
            'ResearchProjectInternalFolder',
            'ResearchProjectList',
            'File',
            'PhotoAlbum',
            'BibliographyList',
	    'BibliographyTopic',
            'ATPhotoAlbum',
	    'Link',
	    'File',
	    'Topic',
	    'MemberInfo',
	    'MemberList',
    ),    
    'allowed_content_types_researchprojectinternalfolder': (
            'ResearchSubproject',
            'Document',
            'Image',
            'ResearchProjectInternalFolder',
            'ResearchProjectList',
            'File',
            'PhotoAlbum',
            'BibliographyList',
	    'BibliographyTopic',
            'ATPhotoAlbum',
            'Ploneboard',
	    'Link',
	    'Event',
	    'News Item',
	    'File',
	    'Topic',
	    'MemberInfo',
	    'MemberList',
    ),    
  }
