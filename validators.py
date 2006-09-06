#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

from Products.CMFCore import permissions
try:
    pass
except ImportError:
    # No multilingual support
    pass

from Products.validation.interfaces.IValidator import IValidator
from Products.validation.validators.BaseValidators import protocols, EMAIL_RE
from Products.validation.validators.RegexValidator import RegexValidator
from Products.validation.validators.RegexValidator import ignoreRE
from Products.validation import validation

from config import atrp_extended_fieldstructure_tags

import re
from types import ListType, StringType

class RegexListValidator(RegexValidator):
    """
    Tests a list of expressions for the same validation type using the RegexValidator.
    """
    __implements__ = IValidator
    
    def __call__(self, valuelist, *args, **kwargs):
    
        if type(valuelist) != ListType:
            return ("Validation failed(%(name)s): %(valuelist)s of type %(type)s, expected 'list'" %
                    { 'name' : self.name, 'valuelist': valuelist, 'type' : type(valuelist)})
        else:
	    for value in valuelist: 
		ignore = kwargs.get('ignore', None)
                if ignore:
    	    	    value = ignoreRE(value, ignore)
		elif self.ignore:
    		    value = ignoreRE(value, self.ignore)

                for r in self.regex:
    	            m = r.match(value)
    		    if not m:
        	        return ("Validation failed(%(name)s): '%(value)s' %(errmsg)s' " %
            		        { 'name' : self.name, 'value': value, 'errmsg' : self.errmsg})

            return 1

BaseListValidators = [
    RegexListValidator('areDecimals',
 	                r'^([+-]?)(?=\d|\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$',
 	                title='', description='',
	                errmsg='is not a decimal number.'),
    RegexListValidator('areInts', r'^([+-])?\d+$', title='', description='',
                        errmsg='is not an integer.'),
    RegexListValidator('arePrintables', r'[a-zA-Z0-9\s]+$', title='', description='',
	                errmsg='contains unprintable characters'),
    RegexListValidator('areSSNs', r'^\d{9}$', title='', description='',
                        errmsg='is not a well formed SSN.'),
    RegexListValidator('areUSPhoneNumbers', r'^\d{10}$', ignore='[\(\)\-\s]',
                        title='', description='',
                        errmsg='is not a valid us phone number.'),
    RegexListValidator('areInternationalPhoneNumbers', r'^\d+$', ignore='[\(\)\-\s\+]',
                        title='', description='',
                        errmsg='is not a valid international phone number.'),
    RegexListValidator('areZipCodes', r'^(\d{5}|\d{9})$',
                        title='', description='',
                        errmsg='is not a valid zip code.'),
    RegexListValidator('areEmails', '^'+EMAIL_RE,
                        title='', description='',
                        errmsg='is not a valid email address.'),
    RegexListValidator('areMailtos', '^mailto:'+EMAIL_RE,
                         title='', description='',
                         errmsg='is not a valid email address.'),
    RegexListValidator('areUnixLikeNames', r"^[A-Za-z][\w\d\-\_]{0,7}$",
                        title="", description="",
                        errmsg="this name is not a valid identifier"),
    RegexListValidator('areURLsOrHaveURLTags', r'(((%s)s?://[^\s\r\n]+)|(.*\ <url:(%s)s?://[^\s\r\n]+>))' % ('|'.join(protocols),'|'.join(protocols)),
    	                title='', description='',
	                errmsg='is / has an invalid URL / URL tag: %s.' % str(protocols)),
    RegexListValidator('haveValidCharacters', r'((^[^<>]+$)|(^.*<.*:.*>))', 
    	                title='', description='',
	                errmsg='has either of the reserved characters < or >.'),
    RegexListValidator('haveValidExtendedFieldstructureTags', r'^(<(%s):.*>)|(.*((\ <(%s):.*>)|[^<>]+))$' % ('|'.join(atrp_extended_fieldstructure_tags), '|'.join(atrp_extended_fieldstructure_tags)), 
    	                title='', description='',
	                errmsg='has an invalid extended field structure tag: %s.' % str(atrp_extended_fieldstructure_tags)),
]						

for service in BaseListValidators:
    validation.register (service) 
										          