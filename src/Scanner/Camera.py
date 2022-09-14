import cv2
import Constants as CONSTANT
from pyzbar.pyzbar import decode
from Tools.JSONTools import read_json, write_json
from datetime import date, datetime
from ast import Constant


class Camera:
    def __init__(self):
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

            processedImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            detectedBarcodes = decode(processedImage)
            if detectedBarcodes and lastDetected > 50:
                barcode = detectedBarcodes[0]
                lastDetected = 0
                value = int(barcode.data)
                user = self.change_user_attendance(value)
                if user is not None:
                    msg = "Welcome " + user + "!"
                else:
                    msg = "Invalid User ID: " + str(value)
                recognizedFrame = frame.copy()
                cv2.putText(recognizedFrame, msg, CONSTANT.bottomLeftCornerOfText,
                            CONSTANT.font, CONSTANT.fontScale, CONSTANT.fontColor, CONSTANT.thickness, CONSTANT.lineType)
                cv2.imshow('scanned', recognizedFrame)
            cv2.imshow('Live Feed', frame)
            if cv2.waitKey(1) == ord('q'):
                break

            if cv2.getWindowProperty('Live Feed', cv2.WND_PROP_VISIBLE) < 1:
                break
        self.vid.release()
        cv2.destroyAllWindows()

    def add_date(self):
        file_data = read_json()
        if len(file_data["members"]) > 0:
            for member in file_data["members"]:
                if self.date_string not in member["days-attended"]:
                    member["days-attended"][self.date_string] = []
        write_json(file_data)

    def change_user_attendance(self, id_num):
        name = None
        file_data = read_json()
        for member in file_data["members"]:
            if member["ID"] == id_num:
                name = member["Name"]
                member["days-attended"][self.date_string].append(datetime.now().strftime("%H:%M:%S"))
        write_json(file_data)
        return name
