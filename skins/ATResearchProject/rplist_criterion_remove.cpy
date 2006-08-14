## Controller Python Script "criterion_remove"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=criterion_ids=[]
##title=ResearchProjectList Criterion Remove

REQUEST=context.REQUEST
from Products.CMFPlone import transaction_note

remove=[]

criteria = context.listCriteria()
for crit in criteria:
    id  = crit.getId()

    if id in criterion_ids:
        remove.append(id) 
        
context.deleteCriterion(remove)

msg = 'Removed criterion(s) %s' % ','.join(remove)
transaction_note(msg)

return state.set(portal_status_message=msg)
