import threading

from main import FullNameProviderHTTPServer

def before_scenario(context, scenario):
    context.server = FullNameProviderHTTPServer()
    context.server_thread = threading.Thread(target=context.server.start)
    context.server_thread.start()

def after_scenario(context, scenario):
    context.server.stop()
    context.server_thread.join()
