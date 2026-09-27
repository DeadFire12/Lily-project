TOOL={'name':'example_action','description':'Safe example bundled action.','version':'1.0'}
def run(context,args): return {'message':"Hello from Lily's action loader.",'arguments':list(args or [])}
