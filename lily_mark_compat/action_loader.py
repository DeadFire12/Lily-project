from __future__ import print_function
import os, imp

class ActionLoader(object):
    def __init__(self,directory): self.directory=os.path.abspath(directory); self.actions={}
    def discover(self):
        self.actions={}
        if not os.path.isdir(self.directory): return self.actions
        for filename in sorted(os.listdir(self.directory)):
            if not filename.endswith('.py') or filename.startswith('_'): continue
            try:
                path=os.path.join(self.directory,filename)
                module=imp.load_source('lily_mark_action_'+os.path.splitext(filename)[0],path)
                meta=getattr(module,'TOOL',None)
                if not isinstance(meta,dict) or not callable(getattr(module,'run',None)): continue
                name=str(meta.get('name') or os.path.splitext(filename)[0])
                self.actions[name]={'name':name,'description':str(meta.get('description') or ''),'module':module,'filename':filename,'enabled':True,'error':None}
            except Exception as exc:
                name=os.path.splitext(filename)[0]
                self.actions[name]={'name':name,'description':'','module':None,'filename':filename,'enabled':False,'error':str(exc)}
        return self.actions
    def list_actions(self):
        return [{k:v[k] for k in ('name','description','filename','enabled','error')} for v in self.actions.values()]
    def run(self,name,context=None,args=None):
        item=self.actions.get(name)
        if item is None: return {'success':False,'error':'Action not found: '+name}
        if not item['enabled'] or item['module'] is None: return {'success':False,'error':item['error'] or 'Action disabled.'}
        try: return {'success':True,'action':name,'result':item['module'].run(context or {},args or [])}
        except Exception as exc: return {'success':False,'action':name,'error':str(exc)}
