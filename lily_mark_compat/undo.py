class UndoStack(object):
    def __init__(self,limit=50): self.limit=int(limit); self._items=[]
    def push(self,description,undo_function):
        self._items.append({'description':str(description),'undo':undo_function})
        if len(self._items)>self.limit: self._items.pop(0)
    def can_undo(self): return bool(self._items)
    def describe(self): return [x['description'] for x in reversed(self._items)]
    def undo(self):
        if not self._items: return {'success':False,'error':'Nothing to undo.'}
        item=self._items.pop()
        try: return {'success':True,'description':item['description'],'result':item['undo']()}
        except Exception as exc: return {'success':False,'description':item['description'],'error':str(exc)}
