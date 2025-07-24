from pichayon.utils import program_options
from pichayon import web
from livereload import Server


def main():
    options = program_options.get_program_options(default_port=8080)

    app = web.create_app()

    program_options.initial_profile(app, options)

    app.debug = options.debug

    server = Server(app.wsgi_app)
    server.watch("pichayon/web")
    server.serve(
        debug=options.debug,
        host=options.host,
        port=int(options.port),
        restart_delay=2,
        open_url_delay=3,
    )

    # app.run(debug=options.debug, host=options.host, port=int(options.port))
