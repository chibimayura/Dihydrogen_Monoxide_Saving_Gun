import cv2
#video 640.0 x 480.0
import requests

# Method to draw boundary around the detected feature
def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text):
    # Converting image to gray-scale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # detecting features in gray-scale image, returns coordinates, width and height of features
    features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)
    coords = []
    # drawing rectangle around the feature and labeling it
    for (x, y, w, h) in features:
        cv2.rectangle(img, (x,y), (x+h, y+h), color, 2)
        cv2.putText(img, text, (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
        coords = [x, y, w, h]


    return coords

def getLoc():
    color = {"blue":(255,0,0), "red":(0,0,255), "green":(0,255,0), "white":(255,255,255)}
    coords = draw_boundary(img, mouthCascade, 3.5, 15, color['green'], "Spray Water Here")
    thirds = 600/3

    if(coords != []):
        x_pos = coords[0]
        if(x_pos < thirds):
            return -1 #left
        elif(x_pos < (thirds*2)):
            return 0 #center
        elif(x_pos >= (thirds*2)):
            return 1 #right

def getHeight():
    color = {"blue":(255,0,0), "red":(0,0,255), "green":(0,255,0), "white":(255,255,255)}
    coords = draw_boundary(img, mouthCascade, 3.5, 15, color['green'], "Spray Water Here")

    if(coords != []):
        return coords[1]



# Loading classifiers
mouthCascade = cv2.CascadeClassifier('haarcascade_mouth.xml')

# Capturing real time video stream. 0 for built-in web-cams, 0 or -1 for external web-cams
video_capture = cv2.VideoCapture(-1)

cur_pos = 0
position = 0
capture_once = False
loc = ""

initial_mouth = 0
end_mouth = 0
is_open = False
mouth_pos = is_open

while True:
    # Reading image from video stream
    _, img = video_capture.read()

    # Call method we defined above

    #trying to get mouth height
    if(not capture_once and getHeight()):
        initial_mouth = getHeight()
        print(type(initial_mouth))

        position = getLoc()
        capture_once = True

    if(getHeight()):
        end_mouth = getHeight()

    cur_pos = getLoc()

    if (position != cur_pos or (initial_mouth != end_mouth and getHeight())):
        position = cur_pos
        if (position == 1 and loc != "right"):
            loc = "right"
            print(loc, position, mouth_pos)
            # requests.post("http://172.31.32.74:3000/", data={"position": position, "location": loc, "is_open": mouth_pos})
        elif (position == 0 and loc != "center"):
            loc = "center"
            print(loc, position, mouth_pos)
            # requests.post("http://172.31.32.74:3000/", data={"position": position, "location": loc, "is_open": mouth_pos})
        elif (position == -1 and loc != "left"):
            loc = "left"
            print(loc, position, mouth_pos)
            # requests.post("http://172.31.32.74:3000/", data={"position": position, "location": loc, "is_open": mouth_pos})

    if(initial_mouth != end_mouth and getHeight()):
        if(abs(initial_mouth - end_mouth) < 20 or abs(initial_mouth - end_mouth)> 60):
            is_open = False
            initial_mouth = end_mouth
            if(is_open != mouth_pos):
                mouth_pos = is_open
                print(loc, position, mouth_pos)
                # requests.post("http://172.31.32.74:3000/", data={"position": position, "location": loc, "is_open": mouth_pos})
        else:
            is_open = True
            if(is_open != mouth_pos):
                mouth_pos = is_open
                print(loc, position, mouth_pos)
                # requests.post("http://172.31.32.74:3000/", data={"position": position, "location": loc, "is_open": mouth_pos})

            
        # if (getHeight() and abs(initial_mouth - end_mouth) < 20 or abs(initial_mouth - end_mouth) > 60):
        #     is_open = False
        #     initial_mouth = end_mouth
        #     if (is_open != mouth_pos):
        #         mouth_pos = is_open
        #         print(mouth_pos)
        #         # requests.post("http://172.31.32.74:3000/", data={"position": position, "location": loc, "is_open": mouth_pos})
        # else:
        #     is_open = True
        #     if (is_open != mouth_pos):
        #         mouth_pos = is_open
        #         print(mouth_pos)
        #         # requests.post("http://172.31.32.74:3000/", data={"position": position, "location": loc, "is_open": mouth_pos})


    # Writing processed image in a new window
    cv2.imshow("face detection", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# class VideoCamera(object):
#     def __init__(self):
#         self.video = cv2.VideoCapture(-1)
#         self.capture_once = False
#         self.cur_pos = 0
#         self.pos = 0
#
#     def __del__(self):
#         self.video.release()
#
#     def get_frames(self):
#         _, img = self.video.read()
#         # cv2.imshow("face detection", img)
#         ret, jpeg = cv2.imshow("face detection", img)
#
#         return jpeg.tobytes()
#
#
# @app.route('/', methods=['GET'])
# def face_det():
#         return "Hello World"
#
# def gen(camera):
#     while True:
#         frame = camera.get_frames()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
#
#
# @app.route('/video_feed')
# def video_feed():
#     return Response(gen(VideoCamera()),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')
#
#
# if __name__ == '__main__':
#     app.run()


# releasing web-cam
video_capture.release()
# Destroying output window
cv2.destroyAllWindows()
