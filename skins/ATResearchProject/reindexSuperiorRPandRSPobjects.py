## Script (Python) "reindexSuperiorRPandRSPobjects.py"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=

from Products.CMFCore.permissions import ModifyPortalContent
if here.portal_type == 'ResearchSubproject' and here.portal_membership.checkPermission(ModifyPortalContent, here):

superior_object = here.aq_inner.aq_parent
portal_object = here.portal_url.getPortalObject()

while (superior_object.portal_portal_type != 'ResearchProject') and (superior_object != portal_object):

    if superior_object.portal_type == 'ResearchSubproject':
	superior_object.reindexObject()
    superior_object = superior_object.aq_inner.aq_parent
    
if superior_object.portal_type == 'ResearchProject':
    superior_object.reindexObject()

