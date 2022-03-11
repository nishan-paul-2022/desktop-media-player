import cv2
import numpy as np


class Yolo2:

    def __init__(self):
        self.net = cv2.dnn.readNetFromDarknet('model/m2_yolo_cross_hands_tiny.cfg', 'model/m2_yolo_cross_hands_tiny.weights')
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

        self.labels = ['hand']
        self.color = (0, 255, 255)
        self.font = cv2.FONT_HERSHEY_PLAIN

    def yolo(self, frame):
        height, width = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), swapRB=True, crop=False)
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

        results = []
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                id = class_ids[i]
                label = self.labels[id]
                confidence = confidences[i]
                results.append((label, confidence, x, y, w, h))

        results.sort(key=lambda x: x[2])
        hand_count = len(results)

        for detection in results[:hand_count]:
            label, confidence, x, y, w, h = detection
            cv2.rectangle(frame, (x, y), (x+w, y+h), self.color, 2)
            cv2.putText(frame, f'{label}', (x + int(w/10), y + int(h/2)), self.font, 1, self.color, 2)
            cv2.putText(frame, f'{confidence}', (x + int(w/10), y + int(h/5)), self.font, 1, self.color, 2)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame