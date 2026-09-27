def register(plugin_manager):
    
    plugin_manager.register(
        "hello_plugin",
        "A simple example plugin.",
        hello
    )


def hello():

    return "Hello from Lily's plugin system! ❤️"