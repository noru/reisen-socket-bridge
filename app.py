from flask import Flask, send_from_directory, render_template
from flask_socketio import SocketIO, emit
from geometry_msgs.msg import Twist
import rospy

app = Flask(__name__)
socketio = SocketIO(app)

linear_speed = 0.3
angular_speed = 1.4
publisher = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
rospy.init_node('reisen_socket_bridge')

def sendTwist(direction):
    twist = Twist()
    if ('up' in direction):
        twist.linear.x = linear_speed
    if ('down' in direction):
        twist.linear.x = -linear_speed
    if ('left' in direction):
        twist.angular.z = angular_speed
    if ('right' in direction):
        twist.angular.z = -angular_speed
    publisher.publish(twist)


@app.route('/')
def index():
    return send_from_directory('', 'index.html')

@app.route('/assets/<path:path>')
def send_js(path):
    return send_from_directory('assets', path)

@socketio.on('key-pressed')
def handle_key_press(key):
    sendTwist(key)
    emit('response', key)


@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=int('5000'), debug=True)