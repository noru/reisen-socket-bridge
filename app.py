#!/usr/bin/env python
from flask import Flask, send_from_directory, render_template
from flask_socketio import SocketIO, emit
from geometry_msgs.msg import Twist
import rospy

app = Flask(__name__)
socketio = SocketIO(app)

linear_speed = 0.2
angular_speed = 1.0
linear_range = [0.2, 2.5]
angular_range = [1.0, 2.5]
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

@app.after_request
def add_header(response):
    response.cache_control.max_age = 0
    return response

@socketio.on('key-pressed')
def key_press(key):
    sendTwist(key)
    emit('response', key)

@socketio.on('set-speed')
def set_speed(linear, angular):
    global linear_speed, angular_speed
    linear_speed = linear_range[0] + (linear_range[1] - linear_range[0]) * int(linear) / 100
    angular_speed = angular_range[0] + (angular_range[1] - angular_range[0]) * int(angular) / 100
    emit('response','linear/angluar speed set to: ' + str(linear_speed) + '/' + str(angular_speed))

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=int('5000'), debug=True)