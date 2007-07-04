from Products.Archetypes.public import process_types, listTypes
from Products.CMFCore import utils as coreutils
from Products.CMFCore.DirectoryView import registerDirectory

from tool.ResearchProjectTool import ResearchProjectSiteConfiguration

# import validators before the module aliases
import validators

# this is for compatibility to versions before 0.3.6rc4
import modulealiases

from config import SKINS_DIR, GLOBALS, PROJECTNAME
from config import ADD_CONTENT_PERMISSION

registerDirectory(SKINS_DIR, GLOBALS)

def initialize(context):

    ##Import Types here to register them
    from content import ResearchProject, ResearchSubproject, ResearchProjectList, ResearchField, ResearchProjectInternalFolder

    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    coreutils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)

    coreutils.ToolInit(
        'ATResearchProject Tool',
	tools		   = (ResearchProjectSiteConfiguration,),
	product_name 	   = PROJECTNAME,
        #icon               = 'tool.gif',
	icon		   = 'skins/ATResearchProject/atrp_tool_icon.gif',
        ).initialize(context)


