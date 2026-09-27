from __future__ import print_function
import os, imp, traceback

class PluginRecord(object):
    def __init__(self, name, description, version, module, filename, enabled=True, error=None):
        self.name=name; self.description=description; self.version=version
        self.module=module; self.filename=filename; self.enabled=enabled; self.error=error
    def to_dict(self):
        return {"name":self.name,"description":self.description,"version":self.version,
                "filename":self.filename,"enabled":self.enabled,"error":self.error}

class PluginLoader(object):
    def __init__(self, directory):
        self.directory=os.path.abspath(directory); self.plugins={}
    def discover(self):
        self.plugins={}
        if not os.path.isdir(self.directory): return self.plugins
        for filename in sorted(os.listdir(self.directory)):
            if not filename.endswith('.py') or filename.startswith('_'): continue
            path=os.path.join(self.directory,filename)
            try:
                module=imp.load_source('lily_mark_plugin_'+os.path.splitext(filename)[0],path)
                meta=getattr(module,'PLUGIN',None)
                if not isinstance(meta,dict): raise ValueError('PLUGIN dictionary is missing.')
                if not callable(getattr(module,'run',None)): raise ValueError('run(context,args) is missing.')
                name=str(meta.get('name') or os.path.splitext(filename)[0])
                self.plugins[name]=PluginRecord(name,str(meta.get('description') or ''),str(meta.get('version') or '1.0'),module,filename)
            except Exception as exc:
                name=os.path.splitext(filename)[0]
                self.plugins[name]=PluginRecord(name,'','',None,filename,False,str(exc))
        return self.plugins
    def list_plugins(self): return [p.to_dict() for p in self.plugins.values()]
    def run(self,name,context=None,args=None):
        p=self.plugins.get(name)
        if p is None: return {'success':False,'error':'Plugin not found: '+name}
        if not p.enabled or p.module is None: return {'success':False,'error':p.error or 'Plugin disabled.'}
        try: return {'success':True,'plugin':name,'result':p.module.run(context or {},args or [])}
        except Exception as exc: return {'success':False,'plugin':name,'error':str(exc),'traceback':traceback.format_exc()}
