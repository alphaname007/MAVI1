from cv2 import destroyAllWindows
from threading import Thread
from flask import Flask, render_template, request, Response
from time import sleep

from mavi1 import MAVI1
from modes import *

mavi:MAVI1 = None

stop = False

modes_names = ["find_target", "get_distance", "use_compass"]
mode = 0

app = Flask(__name__)

@app.route("/")
def default_route():
    return render_template("index.html")

@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
def gen_frames():  
    while True:
        success, frame = mavi.get_frame()
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/info_bar")
def info_bar():
    return Response(gen_info_bar(), mimetype="text/event-stream")
def gen_info_bar():
    while True:
        info_bar = f"⇄:{mavi.get_angle_x()}, ⇅:{mavi.get_angle_y()}, ⇔:{mavi.get_distance()}"
        yield "data: {}\n\n".format(info_bar)
        time.sleep(0.5)

@app.route("/change_mode/", methods=["POST"])
def change_mode():
    global mode

    data = request.get_json()
    if data.get("mode") in modes_names:
        mode = modes_names.index(data.get("mode"))

        print(f"changed mode to {data.get('mode')}")
        return Response(f"changed mode to {data.get('mode')}", 200)
    else:
        return Response(f"no mode {data.get('mode')}", 404)


def main_loop():
    MODE_start_up(mavi)
    with app.app_context():
        while not stop:
            if mode == 0:
                MODE_find_target()
            elif mode == 1:
                MODE_distance
            elif mode == 2:
                MODE_use_compass()
            
            #turbo.push(turbo.replace(render_template('index.html'), 'info_bar'))
            turbo.update(render_template('index.html'), target='info_bar')

            time.sleep(0)


if __name__ == "__main__":

    print("starting MAVI1")
    mavi:MAVI1 = MAVI1(led_count=20)
    MODE_start_up(mavi)
    print("starting Webserver")
    app.run(debug=True, port=8080, host="0.0.0.0")
    print("started Webserver")

    print("starting Glasses")
    change_mode(modes_names[0])
    main_loop_thread = Thread(target=main_loop)
    main_loop_thread.start()

    print("started MAVI completely")
        




