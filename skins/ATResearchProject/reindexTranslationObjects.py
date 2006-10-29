## Script (Python) "reindexSuperiorRPandRSPobjects.py"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=objects=None
##title=

if not objects:
    objects = [ context ]

#from Products.CMFCore.utils import getToolByName
for object in objects:
    if object.isTranslatable() and (object.portal_type in ('ResearchProject', 'ResearchSubproject')):
    
	translations = object.getTranslations()
	for lp_obj in [ translations[key][0] for key in translations.keys() if translations[key][0].UID() != object.UID() ]:
	    if lp_obj.portal_type == 'ResearchProject':
		lp_obj.reindexObject(idxs=['getResearchProjectInfoFields',])
    	    if lp_obj.portal_type == 'ResearchSubproject':
		lp_obj.reindexObject(idxs=['getResearchProjectInfoFields', 'getResearchSubprojectInfoFields'])
