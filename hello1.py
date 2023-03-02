from flask import Flask, render_template, Response,send_file
import cv2
import json
import base64

app = Flask(__name__)

def jetsonCamera(capture_width=1280, capture_height=720, display_width=640, display_height=360, framerate=60, flip_method=0):
    return ('nvarguscamerasrc ! '
            'video/x-raw(memory:NVMM), '
            'width=(int)%d, height=(int)%d, '
            'format=(string)NV12, framerate=(fraction)%d/1 ! '
            'nvvidconv flip-method=%d ! '
            'video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! '
            'videoconvert ! '
            'video/x-raw, format=(string)BGR ! '
            'appsink' % (capture_width, capture_height, framerate, flip_method, display_width, display_height))

camera = cv2.VideoCapture(jetsonCamera(flip_method=0), cv2.CAP_GSTREAMER)

def byte_frames():
    while True:
        success, frame = camera.read()
        print(success)
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpeg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')



@app.route('/byte_photo')
def stream():
    return Response(byte_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True,debug=True)

'''
def take_photo():
    camera = cv2.VideoCapture('nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)1920, height=(int)1080,format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! appsink', cv2.CAP_GSTREAMER)
 
    ret, frame = camera.read()

    if ret:
        cv2.imwrite("photo.jpeg", frame)

    camera.release()

    img = cv2.imread('./photo.jpeg')
 
    image_string = cv2.imencode('.jpeg', img)[1]
 
    image_string = base64.b64encode(image_string,'utf-8').decode()

    dict = {'img':image_string}
 
    with open('./cv2string.json', 'w') as fp:
        json.dump(dict, fp, indent=5)
    
    return json.dumps(dict, fp, indent=5)


@app.route('/take_photo',methods=['GET'])
def video_feed():
    take_photo()
    path="photo.jpeg"
    return send_file(path,as_attachment=True)

'''





