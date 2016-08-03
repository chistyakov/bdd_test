import threading

from main import FullNameProviderHTTPServer, FullNameProviderRequestHandler

def before_scenario(context, scenario):
    context.server = FullNameProviderHTTPServer(('', 8080),
            FullNameProviderRequestHandler)
    context.server_thread = threading.Thread(target=context.server.serve_forever)
    context.server_thread.start()

def after_scenario(context, scenario):
    context.server.shutdown()
    context.server_thread.join()
