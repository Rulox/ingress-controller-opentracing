import logging
from jaeger_client import Config
from opentracing.propagation import Format

from flask_opentracing import FlaskTracing
from flask import Flask, request


JAEGER_HOST = 'jaeger-agent.default.svc.cluster.local'
JAEGER_PORT = '6831'

if __name__ == '__main__':
    app = Flask(__name__)
    log_level = logging.DEBUG
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(asctime)s %(message)s', level=log_level)
    config = Config(config={'sampler': {'type': 'const', 'param': True},
                            'logging': True,
                            'local_agent':
                            {'reporting_host': JAEGER_HOST, 'reporting_post': JAEGER_PORT}},
                    service_name="opentracing_server_app")
    jaeger_tracer = config.initialize_tracer()
    tracing = FlaskTracing(jaeger_tracer)

    @app.route('/trace')
    @tracing.trace()
    def trace():
        with jaeger_tracer.start_active_span('trace method (Flask app)') as scope:
            scope.span.log_kv({'event': 'event log', 'message': "example message created in Server App"})
            return "Success :)"

    app.run(debug=True, host='0.0.0.0', port=5000)
