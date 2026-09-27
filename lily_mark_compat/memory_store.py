from __future__ import print_function
import json, os, re, time, uuid

def _norm(s): return re.sub(r'\s+',' ',str(s or '').lower()).strip()
def _tokens(s): return set(re.findall(r'[a-z0-9_]+',_norm(s)))

class MemoryStore(object):
    def __init__(self,path): self.path=os.path.abspath(path); self.data={'version':1,'memories':[]}; self.load()
    def load(self):
        if not os.path.exists(self.path): return self.data
        try:
            with open(self.path,'r') as f: x=json.load(f)
            if isinstance(x,dict) and isinstance(x.get('memories'),list): self.data=x
        except Exception: pass
        return self.data
    def save(self):
        folder=os.path.dirname(self.path)
        if folder and not os.path.isdir(folder): os.makedirs(folder)
        tmp=self.path+'.tmp'
        with open(tmp,'w') as f: json.dump(self.data,f,indent=2)
        if os.path.exists(self.path): os.remove(self.path)
        os.rename(tmp,self.path)
    def add(self,text,category='general',source='user'):
        item={'id':uuid.uuid4().hex,'text':str(text),'category':str(category),'source':str(source),'created':time.time(),'updated':time.time()}
        self.data['memories'].append(item); self.save(); return item
    def search(self,query,limit=10):
        q=_tokens(query); scored=[]
        for item in self.data.get('memories',[]):
            score=len(q.intersection(_tokens(item.get('text',''))))
            if score: scored.append((score,item))
        scored.sort(key=lambda x:(-x[0],-float(x[1].get('updated',0))))
        return [x[1] for x in scored[:int(limit)]]
    def list_all(self): return list(self.data.get('memories',[]))
    def delete(self,memory_id):
        old=self.data.get('memories',[]); new=[x for x in old if x.get('id')!=memory_id]
        if len(old)==len(new): return False
        self.data['memories']=new; self.save(); return True
