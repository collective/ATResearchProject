try:

  from Products.LinguaPlone.public import listTypes
except:
  # no multilingual support
  from Products.Archetypes.public import listTypes
  
from Products.Archetypes.Extensions.utils import installTypes, install_subskin

from Products.CMFCore.utils import getToolByName

from Products.ATResearchProject.config import PROJECTNAME
from Products.ATResearchProject.config import ATRP_TOOL_ID
from Products.ATResearchProject.config import ATRP_TOOL_NAME
from Products.ATResearchProject.config import GLOBALS
from Products.ATResearchProject.config import DEPARTMENT_DEFAULTS
from Products.ATResearchProject.config import ALLOWED_CT_DEFAULTS
from Products.ATResearchProject.config import CATALOG_INDEXES
from Products.ATResearchProject.config import CATALOG_METADATA

from StringIO import StringIO

def setupTool(self, out):
    """
    adds the research project site configuration tool to the portal root folder
    """
    if hasattr(self, ATRP_TOOL_ID):
        self.manage_delObjects([ATRP_TOOL_ID])
        out.write('Deleting old tool; make sure you repeat customizations.')
    addTool = self.manage_addProduct[PROJECTNAME].manage_addTool
    addTool(ATRP_TOOL_NAME, None)
    out.write("\nAdded the research project site configuration tool to the portal root folder.\n")
    atrp_tool = getToolByName(self, ATRP_TOOL_ID)
    acttool = getToolByName(self, 'portal_actions')
    acttool.addActionProvider(ATRP_TOOL_ID)
    out.write("Registered the research project tool as an action provider.\n")
    
    # add/modify DEPARTMENT default properties
    atrp_tool.manage_changeProperties(DEPARTMENT_DEFAULTS)
    for dictItem in DEPARTMENT_DEFAULTS.keys():
      if not atrp_tool.hasProperty(dictItem):
        atrp_tool.manage_addProperty(dictItem, DEPARTMENT_DEFAULTS[dictItem], 'lines')

    out.write("Set default properties at the research project site configuration tool.\n")

def addPrefsPanel(self, out):
    cp = getToolByName(self, 'portal_controlpanel', None)
    if not cp:
        out.write ("No control panel found. Skipping installation of the setup panel.\n")
    else:
	cp.addAction(id='ResearchProjectSiteConfiguration',
                     name=ATRP_TOOL_NAME+' (ZMI for now)',
		     action='string:${portal_url}/prefs_atrptool_info',
	 	     permission='Manage portal',
		     category='Products',
		     appId=PROJECTNAME,
		     imageUrl='atrp_tool_icon.gif',
		     description='Side-wide configuration for the ATResearchProject content types.')
	out.write ("Installed the research project site configuration tool into the control panel.\n")

def addToFactoryTool(self, out):
    # make new types use portal_factory
    ftool = getToolByName(self, 'portal_factory')
    if ftool:
	portal_factory_types = ftool.getFactoryTypes().keys()
	for portalType in [ typeDict['portal_type'] for typeDict in listTypes(PROJECTNAME) ]:
    	    if portalType not in portal_factory_types:
		portal_factory_types.append(portalType)
        ftool.manage_setPortalFactoryTypes(listOfTypeIds=portal_factory_types)
	print >> out, 'New types use portal_factory'

def addIndexesToCatalogTool(self, out):
    ctool = getToolByName(self, 'portal_catalog')
    if ctool:
        # add indexes and metadatas to the portal catalog
        ct = getToolByName(self, 'portal_catalog')
        for idx in CATALOG_INDEXES:
            if idx['name'] in ct.indexes():
	        ct.delIndex(idx['name'])
		ct.addIndex(**idx)
		ct.reindexIndex(idx['name'], REQUEST=None)
		out.write("Found the '%s' index in the catalog, reinstalled and reindexed it to make sure the index type correct.\n" % idx['name'])
	    else:
		ct.addIndex(**idx)
		ct.reindexIndex(idx['name'], REQUEST=None)
		out.write("Added and reindexed '%s' (%s) to the catalog.\n" % (idx['name'], idx['type']))
		    
def addMetadataToCatalogTool(self, out):
    ctool = getToolByName(self, 'portal_catalog')
    if ctool:
        # add indexes and metadatas to the portal catalog
        ct = getToolByName(self, 'portal_catalog')
        for entry in CATALOG_METADATA:
	    if entry in ct.schema():
	        out.write("Found '%s' in the catalog metadatas, nothing changed.\n" % entry)
	    else:
	        ct.addColumn(entry)
	        out.write("Added '%s' to the catalog metadatas.\n" % entry)

def install(self):
    out = StringIO()
 
    setupTool(self, out)
    addPrefsPanel(self, out)
 
    installTypes(self, out, listTypes(PROJECTNAME), PROJECTNAME)
    out.write('%s\n' % listTypes(PROJECTNAME))
    addToFactoryTool(self, out)
    addIndexesToCatalogTool(self, out)
    addMetadataToCatalogTool(self, out)
    
    install_subskin(self, out, GLOBALS)

    out.write("Successfully installed %s." % PROJECTNAME)
    return out.getvalue()

def removeFromActionProviders(self, out):
    """
    removes portal_researchproject from the action providers
    registered with the action tool
    """
    acttool = getToolByName (self, 'portal_actions')
    if ATRP_TOOL_ID in acttool.listActionProviders():
      acttool.deleteActionProvider(ATRP_TOOL_ID)

def removePrefsPanel(self, out):
    cp = getToolByName(self, 'portal_controlpanel', None)
    if cp:
      cp.unregisterApplication(PROJECTNAME)
      
def removeIndexesFromCatalogTool(self, out):
    ctool = getToolByName(self, 'portal_catalog')
    if ctool:
        # add indexes and metadatas to the portal catalog
        ct = getToolByName(self, 'portal_catalog')
        for idx in CATALOG_INDEXES:
            if idx['name'] in ct.indexes():
	        ct.delIndex(idx['name'])
		out.write("Removed '%s' index from the catalog.\n" % idx['name'])
	    else:
		out.write("Index '%s' (%s) not found in the catalog, nothing changed.\n" % (idx['name'], idx['type']))
		
def removeMetadataFromCatalogTool(self, out):
    ctool = getToolByName(self, 'portal_catalog')
    if ctool:
        # add indexes and metadatas to the portal catalog
        ct = getToolByName(self, 'portal_catalog')
        for entry in CATALOG_METADATA:
	    if entry in ct.schema():
	        ct.delColumn(entry)
		out.write("Found '%s' in the catalog metadatas, removed it.\n" % entry)
	    else:
	        ct.addColumn(entry)
	        out.write("Column '%s' has not been found in the catalog metadatas. Nothing changed.\n" % entry)
									  
def uninstall(self):
    out = StringIO()
    removeFromActionProviders(self, out)
    #removeActions(self)
    removePrefsPanel(self, out)
    removeIndexesFromCatalogTool(self, out)
    removeMetadataFromCatalogTool(self, out)
    # all the rest of cleaning we leave to the quickinstaller
    print >> out, "Uninstalled %s." % PROJECTNAME
    return out.getvalue()
    