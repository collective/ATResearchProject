# Zope imports
from persistent.mapping import PersistentMapping

# CMF imports
from Products.CMFCore.utils import getToolByName

from Products.Archetypes.utils import shasattr
from Products.Archetypes.public import listTypes

# myself
from Products.ATResearchProject.config import PROJECTNAME

ATRP_SCHEMA_MIGRATION = {
    'ResearchProject': { 'new': [ 'researchProjectContactPersons',], 'removed': [ 'researchProjectInfoFields',], },
    'ResearchSubproject': { 'new': [], 'removed': [ 'researchSubprojectInfoFields', ], },
    'ResearchProjectInternalFolder': { 'new': [], 'removed': [], },
    'ResearchProjectList': { 'new': [], 'removed': [], },
    'ResearchField': { 'new': [], 'removed': [], },
}

ATRPLIST_CRITERIA_MIGRATION = [
    { 'old_index': 'researchProjectInfoFields', 'new_index': 'getResearchProjectInfoFields',},
    { 'old_index': 'researchSubprojectInfoFields', 'new_index': 'getResearchSubprojectInfoFields',},
]

class Migration(object):
    """Migrating from UNRELEASED to 0.4

    It *must* be safe to use this multiple times as it is run automatically
    upon (re)install in the portal_quickinstaller.
    """

    def __init__(self, site, out):
        self.site = site
        self.out = out

    def migrate(self):
        """Run migration on site object passed to __init__.
        """
        print >> self.out
	print >> self.out, u"Migrating ATResearchProject UNRELEASED -> 0.4"
	if self.needsGeneralSchemaUpgrade():
    	    self.generalSchemaUpgrade()
	self.migrateATRPListsCriteria()
	    

    def needsGeneralSchemaUpgrade(self):
        """Returns True if one of the first 5 ATRP items found
           has missing schema fields; called by the installer to 
	   figure out whether a schema update is needed."""
        print >> self.out, u"general schema upgrade of ATResearchProject items"
	print >> self.out, u"-------------------------------------------------"
	ctool = getToolByName(self.site, 'portal_catalog')

	for ct in ATRP_SCHEMA_MIGRATION.keys():
	    brains = ctool(portal_type=ct)
	    new_attributes = ATRP_SCHEMA_MIGRATION[ct]['new']
	    removed_attributes =  ATRP_SCHEMA_MIGRATION[ct]['removed']

	    # needs schema upgrade for authors field
	    if brains:
		for attribute in new_attributes:
		    for brain in brains[:10]:
			if not shasattr(brain.getObject(), attribute, False):
			    print 'Schema upgrade because of new attributes'
			    return True
		for attribute in removed_attributes:
		    for brain in brains[:10]:
			if shasattr(brain.getObject(), attribute, False):
			    print 'Schema upgrade because of removed attributes'
			    return True
	
	print >> self.out, u"    No general schema upgrade needed."
	print >> self.out
	
	return False
																								     
    # migrate data from old to new schema
    def generalSchemaUpgrade(self):
        """perform a general AT schema upgrade"""

        # logging to ZLog and to quick installer's report
        print >> self.out, u'    ATResearchProject items need general schema upgrade!!! This might take a while...'
        print u'***'
        print u'*** ATResearchProject migration: ATResearchProject items need general schema upgrade!!! This might take a while...'
        print u'***'
	    
        ctool = getToolByName(self.site, 'portal_catalog')
	atrp_types = [ ct['portal_type'] for ct in listTypes(PROJECTNAME) ]
	brains = ctool(portal_type=atrp_types)
	for brain in brains:
	    obj = brain.getObject()
	    ct = obj.portal_type
	    if ct in ATRP_SCHEMA_MIGRATION.keys():
		for remove_field in ATRP_SCHEMA_MIGRATION[ct]['removed']:
		    delattr(obj, remove_field)
	    obj._updateSchema()
	    
	print u'ATResearchProject migration: Upgraded schemata of %s items' % len(brains)
	print
	print >> self.out, u'    Upgraded schemata of %s items' % len(brains)
	print >> self.out

    def migrateATRPListsCriteria(self):
        """Migrates ATRPList criteria if index ids have changed; called
           by the installer to figure out whether a criteria update
           is needed."""
        print >> self.out, u"Criteria update of of ATResearchProject RPLists"
	print >> self.out, u"-----------------------------------------------"
	ctool = getToolByName(self.site, 'portal_catalog')

	brains = ctool(portal_type='ResearchProjectList')
	count = 0
	if brains:
	    for brain in brains:
		obj = brain.getObject()
		obj_updated = False
		for old_criterion in obj.listCriteria():
		    for migrate_field_dict in ATRPLIST_CRITERIA_MIGRATION:
			if migrate_field_dict['old_index'] in old_criterion.getId():
			    # we assume that the new field may be combined with the same criteria type as the old field
			    new_criterion = obj.addCriterion(field=migrate_field_dict['new_index'], criterion_type=old_criterion.meta_type)
			    new_criterion.setValue(old_criterion.Value())
			    obj.deleteCriterion(old_criterion.getId())
			    obj_updated = True
		if obj_updated:	    
		    count += 1
		
	if count == 0:		
	    print >> self.out, u"    No criteria upgrade needed."
	else:
	    print >> self.out, u"    Upgraded criteria of %s ResearchProjectList items." % count
	print >> self.out
																								     
	