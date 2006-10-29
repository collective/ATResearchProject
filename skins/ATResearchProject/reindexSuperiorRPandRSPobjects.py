## Script (Python) "reindexSuperiorRPandRSPobjects.py"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=

reindexed_objects = []
from Products.CMFCore.permissions import ModifyPortalContent
if (context.portal_type == 'ResearchSubproject') and (context.portal_membership.checkPermission(ModifyPortalContent, context)):

    superior_object = context.aq_inner.aq_parent
    portal_object = context.portal_url.getPortalObject()

    while (superior_object.portal_type != 'ResearchProject') and (superior_object != portal_object):

	if superior_object.portal_type == 'ResearchSubproject':
	    superior_object.reindexObject(idxs=['getResearchProjectInfoFields', 'getResearchSubprojectInfoFields'])
	    reindexed_objects.append(superior_object)
        superior_object = superior_object.aq_inner.aq_parent
    
    if superior_object.portal_type == 'ResearchProject':
	superior_object.reindexObject(idxs=['getResearchProjectInfoFields'])
	reindexed_objects.append(superior_object)

return reindexed_objects