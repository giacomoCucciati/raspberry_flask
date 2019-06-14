from src import create_app, socketio
import logging

logger = logging.getLogger('webgui_logger')
logger.setLevel(logging.DEBUG)

app = create_app(debug=True)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0")
