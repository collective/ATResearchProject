## Script (Python) "research_project_formatCatalogMetadata"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=value,long_format=True
##title=Determine whether the input is a DateTime or ISO date and localize it if so, also convert lists and dicts into reasonable strings.
from DateTime import DateTime
from ZODB.POSException import ConflictError
from Products.CMFPlone.utils import safe_callable
from AccessControl import Unauthorized

if value is None:
    return ''

if same_type(value, DateTime()):
    return context.toLocalizedTime(value.ISO(), long_format = long_format)

# Ugly but fast check for ISO format (ensure we have '-' and positions 4 and 7,
#  ' ' at positiion 10 and ':' and 13 and 16), then convert just in case.
if same_type(value, '') and value[4:-1:3] == '-- ::':
    try:
        DateTime(value)
    except ConflictError:
        raise
    except:
        # Bare excepts are ugly, but DateTime raises a whole bunch of different
        # errors for bad input (Syntax, Time, Date, Index, etc.), best to be
        # safe.
        return value
    return context.toLocalizedTime(value, long_format = long_format)

try:
    # Missing.Value and others have items() but don't have security assertions
    # to support accessing it.
    items = getattr(value, 'items', None)
except Unauthorized:
    items = None

if items is not None and safe_callable(items):
    # For dictionaries return a string of the form 'key1: value1, key2: value2' 
    value = ', '.join(['%s: %s'%(a,b) for a,b in items()])
if same_type(value,[]) or same_type(value,()):
    # Return list as comma separated values
    value = ', '.join([str(v) for v in value])

value = str(value)

return value
