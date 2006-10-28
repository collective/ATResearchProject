# Zope imports
from persistent.mapping import PersistentMapping

# CMF imports
from Products.CMFCore.utils import getToolByName

from Products.Archetypes.utils import shasattr
from Products.Archetypes.public import listTypes

# myself
from Products.ATResearchProject.config import PROJECTNAME

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
	self.migrateATRPListsCriteria()

    def migrateATRPListsCriteria(self):
        """Migrates ATRPList criteria if index ids have changed; called
           by the installer to figure out whether a criteria update
           is needed."""
        print >> self.out, u"Criteria update of of ATResearchProject RPLists"
	print >> self.out, u"-----------------------------------------------"
	ctool = getToolByName(self.site, 'portal_catalog')

	brains = ctool(portal_type='ResearchProjectList', Language='all')
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
		    print "Modified criteria list of ResearchProjectList item ,,%s''" % obj.getId()
		    count += 1
		
	if count == 0:		
	    print >> self.out, u"    No criteria upgrade needed."
	else:
	    print >> self.out, u"    Upgraded criteria of %s ResearchProjectList items." % count
	print >> self.out
