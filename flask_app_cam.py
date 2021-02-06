from flask import Flask, request, redirect, url_for, render_template, json, render_template_string, jsonify, Response
from camera import VideoCamera

from pylgbst.hub import TechnicHub
from pylgbst import get_connection_gattool
from pylgbst.peripherals import Motor,EncodedMotor
import time

app = Flask(__name__)

conn = ''
hub = ''
power_direction =''
power_motor =''
inc_dump = 0

@app.route('/', methods=['GET', 'POST'])
def control_panel():
    global conn
    global hub
    global power_direction
    global power_motor
    global inc_dump
    print('request.form:', request.form)
    
    if request.method == 'POST':
        if request.form.get('button') == 'button-play':
            conn = get_connection_gattool(hub_mac='90:84:2B:5F:33:35') #auto connect does not work
            hub = TechnicHub(conn)
            power_direction = EncodedMotor(hub, hub.PORT_B)
            power_motor = EncodedMotor(hub, hub.PORT_D)
            print("play button pressed")

        elif request.form.get('button') == 'button-exit':
            power_motor.stop()
            power_direction.stop()
            conn.disconnect() 
            print("exit button pressed")


        elif request.form.get('slide_direction') or request.form.get('slide_power'):
            direction = request.form.get('slide_direction')
            power = request.form.get('slide_power')
            print('print direction:', direction,'print power:', power)

            if (conn !=''):
                power_motor.start_power(float(power)/100)
                power_direction.start_power(float(direction)/100)
            else:
                print("No connection to hub")

            jsonFile = "dump_{}.json".format(inc_dump)

            with open(jsonFile, "w+") as f:
                json.dump({'direction': direction,'power': power}, f)

            inc_dump = inc_dump + 1
            #return json.dumps({'direction': direction,'power': power})

    return render_template('main.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    #print('video_feed  request.form:', request.form)
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True, use_reloader=False)

