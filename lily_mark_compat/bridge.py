from __future__ import print_function
import os
from .plugin_loader import PluginLoader
from .action_loader import ActionLoader
from .memory_store import MemoryStore
from .confirm import ConfirmationGate
from .undo import UndoStack
from .self_knowledge import build_self_knowledge,format_self_knowledge

class LilyMarkBridge(object):
    def __init__(self,base_dir,assistant_name='Lily'):
        self.base_dir=os.path.abspath(base_dir); self.assistant_name=assistant_name
        root=os.path.join(self.base_dir,'lily_mark_compat')
        self.plugin_loader=PluginLoader(os.path.join(root,'skills'))
        self.action_loader=ActionLoader(os.path.join(root,'actions'))
        self.memory=MemoryStore(os.path.join(root,'memory','memories.json'))
        self.confirmation=ConfirmationGate(); self.undo=UndoStack(); self.self_knowledge={}
    def discover(self):
        p=self.plugin_loader.discover(); a=self.action_loader.discover()
        self.self_knowledge=build_self_knowledge(self.assistant_name,self.plugin_loader.list_plugins(),self.action_loader.list_actions())
        return {'plugins':p,'actions':a,'self_knowledge':self.self_knowledge}
    def describe(self): return format_self_knowledge(self.self_knowledge)
    def status(self): return {'success':True,'assistant':self.assistant_name,'plugins':self.plugin_loader.list_plugins(),'actions':self.action_loader.list_actions(),'memory_count':len(self.memory.list_all()),'can_undo':self.undo.can_undo(),'confirmation_pending':self.confirmation.current() is not None}
