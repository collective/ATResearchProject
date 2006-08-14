## Controller Python Script "criterion_set_sort"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=rp_field, rsp_field, rp_reversed=0, rsp_reversed=0
##title=ResearchProjectList Criterion Set Sort

REQUEST=context.REQUEST
from Products.CMFPlone import transaction_note

for field, reversed, portal_type in ((rp_field, rp_reversed, 'ResearchProject'), (rsp_field, rsp_reversed, 'ResearchSubproject')):

    context.setPortalTypeToQuery(portal_type)
    if field == 'no_sort':
	context.removeSortCriterion()
    else:
	context.setSortCriterion(field, reversed)

msg = 'Sort order set on fields %s / %s' % (rp_field, rsp_field)
transaction_note(msg)

return state.set(portal_status_message=msg)
