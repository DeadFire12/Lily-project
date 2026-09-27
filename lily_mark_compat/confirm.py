import uuid

class ConfirmationGate(object):
    """Creates pending requests only; Lily's existing yes/no loop stays authoritative."""
    def __init__(self): self.pending=None
    def request(self,action,details=None):
        self.pending={'token':uuid.uuid4().hex,'action':str(action),'details':details or {}}
        return {'success':False,'confirmation_required':True,'action':self.pending['action'],'details':self.pending['details'],'token':self.pending['token']}
    def current(self): return self.pending
    def cancel(self): self.pending=None; return {'success':True,'cancelled':True}
    def consume(self,token):
        if not self.pending: return {'success':False,'error':'No confirmation is pending.'}
        if token!=self.pending['token']: return {'success':False,'error':'Invalid confirmation token.'}
        req=self.pending; self.pending=None; return {'success':True,'confirmed':True,'request':req}
