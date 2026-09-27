PLUGIN={'name':'example_skill','description':'Safe example for Lily self-describing skills.','version':'1.0'}
def run(context,args): return {'message':"Hello from Lily's compatibility skill system.",'arguments':list(args or [])}
