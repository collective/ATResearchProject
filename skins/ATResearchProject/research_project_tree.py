## Script (Python) "research_project_tree.py"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
contextPath = context.absolute_url()
projectTypes = ['ResearchProject','ResearchSubproject','ResearchProjectInternalFolder','BibliographyList','BibliographyTopic', 'MemberList',]

def findContextSubtree(objectTree):

  result = {}

  for thisLevelObject in objectTree:
    
    if thisLevelObject.has_key('absolute_url') and thisLevelObject['absolute_url'] == contextPath:
      return [thisLevelObject]
    
    elif thisLevelObject.has_key('absolute_url') and (thisLevelObject['absolute_url'] in contextPath) and (thisLevelObject['absolute_url'] != contextPath):
      result = findContextSubtree(thisLevelObject['children'])

    if result:
      return result

def researchProjectTree(subtree):

  for brainObject in subtree:

    if (brainObject['portal_type'] in projectTypes):
      print '<ul>'
      print '<li style="list-style: none; list-style-image: none;">'
      print '<div class="contenttype-%s visualIconPadding">' % context.plone_utils.normalizeString(brainObject['portal_type'])
      print '<a href="%s"><b class="state-%s">' %  (brainObject['absolute_url'], context.plone_utils.normalizeString(brainObject['review_state']))
      print '%s' % brainObject['Title']
      print '</b></a>'
      print '<div>'
      print '%s' % brainObject['Description']
      print '</div>'
      print '</div>'
      print '</li>'

      if brainObject['children']:
        print researchProjectTree(brainObject['children'])
      
      print '</ul>'

  return printed

     
if context.portal_type in projectTypes:

  html_output = ''
  data = context.getResearchProjectStructure()
  contextSubtree = findContextSubtree([data])

  if contextSubtree and contextSubtree[0].has_key('children') and (len(contextSubtree[0]['children']) >= 1):
      html_output = researchProjectTree(contextSubtree)

  return html_output

else:
  return None
