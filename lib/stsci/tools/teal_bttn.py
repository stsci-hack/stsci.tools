"""teal_bttn.py: for defining the action "parameter" button widget
   to be used in TEAL.

$Id$
"""
from __future__ import division # confidence high

import sys, traceback
import eparoption, vtor_checks

class TealActionParButton(eparoption.ActionEparButton):

    def getButtonLabel(self):
        """ Return string to be used on as button label - "value" of par. """
        # If the value has a comma, return the 2nd part, else use whole thing
        return self.value.split(',')[-1].strip()

    def getShowName(self):
        """ Return string to be used on LHS of button - "name" of par. """
        # If the value has a comma, return the 1st part, else leave empty
        if self.value.find(',') >= 0:
            return self.value.split(',')[0]
        else:
            return ''

    def clicked(self):
        """ Called when this button is clicked. Execute code from .cfgspc """
        try:
            import teal
        except:
            teal = None
        try:
            # start drilling down into the tpo to get the code
            tealGui = self._mainGuiObj
            tealGui.showStatus('Clicked "'+self.getButtonLabel()+'"', keep=1)
            pscope = self.paramInfo.scope
            pname = self.paramInfo.name
            tpo = tealGui._taskParsObj
            tup = tpo.getExecuteStrings(pscope, pname)
            code = ''
            if not tup:
                if teal:
                    teal.popUpErr(tealGui.top, "No action to perform",
                                  "Action Button Error")
                return
            for exname in tup:
                if '_RULES_' in tpo and exname in tpo['_RULES_'].configspec:
                    ruleSig = tpo['_RULES_'].configspec[exname]
                    chkArgsDict = vtor_checks.sigStrToKwArgsDict(ruleSig)
                    code = chkArgsDict.get('code') # a string or None
                    # now go ahead and execute it
                    teal.execEmbCode(pscope, pname, self.getButtonLabel(),
                                     tealGui, code)
            # done
            tealGui.debug('Finished: "'+self.getButtonLabel()+'"')
        except Exception, ex:
            msg = 'Error executing: "'+self.getButtonLabel()+'"\n'+ex.message
            msgFull = msg+'\n'+''.join(traceback.format_exc())
            msgFull+= "CODE:\n"+code
            if tealGui:
                if teal: teal.popUpErr(tealGui.top, msg, "Action Button Error")
                tealGui.debug(msgFull)
            else:
                if teal: teal.popUpErr(None, msg, "Action Button Error")
                print msgFull
