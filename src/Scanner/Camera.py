import cv2
import Constants as CONSTANT
from Tools.JSONTools import read_json, write_json
from datetime import date
from ast import Constant


class Camera:
    def __init__(self):
        self.qr_decoder = cv2.QRCodeDetector()
        self.vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        dateToday = date.today()
        self.date_string = dateToday.strftime("%m-%d-%Y")

        self.add_date()

    def start(self):
        lastDetected = 0
        while True:
            lastDetected += 1

            ret, frame = self.vid.read()

            msg = ""
            data, points, _ = self.qr_decoder.detectAndDecode(frame)
            if data and lastDetected > 50:
                lastDetected = 0
                value = int(data)
                user = self.change_user_attendance(value)
                if user is not None:
                    msg = "Welcome " + user + "!"
                else:
                    msg = "Invalid User ID: " + str(value)
                recognizedFrame = frame.copy()
                cv2.putText(recognizedFrame, msg, CONSTANT.bottomLeftCornerOfText,
                            CONSTANT.font, CONSTANT.fontScale, CONSTANT.fontColor, CONSTANT.thickness, CONSTANT.lineType)
                cv2.imshow('poop', recognizedFrame)
            cv2.imshow('Live Feed', frame)
            if cv2.waitKey(1) == ord('q'):
                break

            if cv2.getWindowProperty('Live Feed', cv2.WND_PROP_VISIBLE) < 1:
                break
        self.vid.release()
        cv2.destroyAllWindows()

    def add_date(self):
        file_data = read_json()
        if len(file_data["members"]) > 0 and self.date_string not in file_data["members"][0]["days-attended"]:
            for member in file_data["members"]:
                member["days-attended"][self.date_string] = False
        write_json(file_data)

    def change_user_attendance(self, id_num):
        name = None
        file_data = read_json()
        for member in file_data["members"]:
            if member["id"] == id_num:
                name = member["name"]
                member["days-attended"][self.date_string] = True
        write_json(file_data)
        return name