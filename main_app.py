from cv2 import destroyAllWindows
from threading import Thread
from flask import Flask, render_template_string, request
from time import sleep

from mavi1 import MAVI1
from modes import *

mavi:MAVI1 = None

message = "started MAVI"
stop = False

modes_names = ["find_target", "get_distance", "compass"]
mode_func = None

app = Flask(__name__)

@app.route("/")
def default_route():
    return """
    
        <!DOCTYPE html>
        <html lang="de">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="X-UA-Compatible" content="ie=edge">
            <title>MAVI</title>
        </head>
        <body>
            <h1>MAVI</h1>
                                  
            <img id="frame">
                                  
            <p id="info_bar">X:10, Y:20, Distance:120</p>

            <div id="button_group">
                <button id="find_target">Find Target</button>
                <button id="get_distance">Get Distance</button>
                <button id="compass">Compass</button>
            </div>
                                  
            <style>
                body{
                    width: 100vw;
                    height: 100vh;
                    color: white;
                    background-color: grey;
                    text-align: center;
                    font-family: sans-serif;
                }
                h1{
                    font-family:monospace;
                    font-size: 10vh;
                }
                p{
                    font-size: 8vh;
                }
                button{
                    background-color: white;
                }
                #button_group{
                    width: 100vw;
                    display: block;
                }
            </style>
        </body>
        </html>
    
    """

@app.route("/change_mode/{mode_name}>", methods=["POST"])
def change_mode(mode_name:str):
    global message
    global mode_func

    if not mode_name in modes_names:
        return False
    else:
        mode_name = f"MODUS_{mode_name}"
        mode_func = locals()[mode_name]

        message = f"changed mode to {mode_name}"



if __name__ == "__main__":

    print("starting MAVI1")
    mavi:MAVI1 = MAVI1(led_count=20)

    print("starting Webserver")
    app.run(debug=True, port=8080, host="0.0.0.0")
    print("started Webserver")
    while True:
        pass

    print("starting Glasses")
    MODE_start_up(mavi)

    print("started MAVI completely")

    change_mode(modes_names[0])

    while not stop:
        time.sleep(0)
        mode_func(mavi)




