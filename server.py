from datetime import datetime, timezone
from flask import Flask, jsonify

def create_app() -> Flask:
    app = Flask(__name__)

    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'trading-bot',
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'message': 'Trading bot is running'
        })

    @app.route('/')
    def root():
        return jsonify({
            'service': 'Jellyfish Trading Bot',
            'status': 'running',
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'endpoints': {
                '/health': 'Health check endpoint',
                '/': 'Root endpoint'
            }
        })

    return app

def run_flask_server():
    app = create_app()
    app.logger.disabled = True
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
