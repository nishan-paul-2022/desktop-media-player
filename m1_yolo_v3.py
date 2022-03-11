import numpy as np
import cv2


class Yolo1:

    def __init__(self):
        self.net = cv2.dnn.readNet('model/m1_yolo_v3_tiny.weights', 'model/m1_yolo_v3_tiny.cfg')  # load yolo
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

        self.f = open('model/m1_coco.names', 'r')
        self.classes = [line.strip() for line in self.f.readlines()]
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))
        self.font = cv2.FONT_HERSHEY_PLAIN

    def yolo(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)  # detecting objects
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)
        class_ids, confidences, boxes = list(), list(), list()

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > 0.4:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 1.8)
                    y = int(center_y - h / 1.8)

                    boxes.append([x, y, w, h])
                    confidences.append(round(float(confidence), 2))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.3)

        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                id = class_ids[i]
                label = str(self.classes[id])
                confidence = confidences[i]
                color = self.colors[id]
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                cv2.putText(frame, f'{label}', (x + int(w/10), y+int(h/2)), self.font, 1, color, 2)
                cv2.putText(frame, f'{confidence}', (x + int(w/10), y+int(h/10)), self.font, 1, color, 2)

        return frame


# https://github.com/muhammadshiraz/YOLO-Real-Time-Object-Detection