from __future__ import print_function
import os, platform

def build_self_knowledge(assistant_name,plugins=None,actions=None):
    plugins=plugins or []; actions=actions or []
    pn=[x.get('name','') for x in plugins if isinstance(x,dict)]
    an=[x.get('name','') for x in actions if isinstance(x,dict)]
    return {'name':assistant_name,'platform':platform.system(),'platform_release':platform.release(),'python':platform.python_version(),'architecture':platform.machine(),'cwd':os.getcwd(),'capabilities':{'plugins':sorted([x for x in pn if x]),'actions':sorted([x for x in an if x])},'limits':['Only discovered capabilities should be claimed.','A screenshot is a point-in-time capture, not continuous vision.','Dangerous actions require human confirmation.','Unknown capabilities should be reported honestly.']}

def format_self_knowledge(info):
    c=info.get('capabilities',{}); return '\n'.join(['Assistant: '+str(info.get('name','Lily')),'OS: %s %s'%(info.get('platform',''),info.get('platform_release','')),'Python: '+str(info.get('python','')),'Architecture: '+str(info.get('architecture','')),'','Actions: '+(', '.join(c.get('actions',[])) or 'none'),'Plugins: '+(', '.join(c.get('plugins',[])) or 'none'),'','Limits:']+['- '+x for x in info.get('limits',[])])
