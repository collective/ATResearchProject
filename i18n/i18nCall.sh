#!/bin/bash
cd ..
i18ndude rebuild-pot --pot i18n/atresearchproject-generated.pot --create atresearchproject --merge i18n/atresearchproject-manual.pot ./skins
#i18ndude rebuild-pot --pot i18n/plone-generated.pot --create plone --merge i18n/plone-manual.pot ./skins
cp i18n/plone-manual.pot i18n/plone-generated.pot
cd i18n
