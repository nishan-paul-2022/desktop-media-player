from m1_yolo_v3 import Yolo1
from m2_yolo_cross_hands import Yolo2
from CustomVideoPlayer import VideoPlayer


def main_not_using_model():
    video = VideoPlayer()
    video.mainloop()


def main_using_model():
    keys = ('m1_yolo_v3', 'm2_yolo_cross_hands')
    values = (Yolo1().yolo, Yolo2().yolo)
    video = VideoPlayer(keys, values)
    video.mainloop()


if __name__ == '__main__':
    main_not_using_model()
    # main_using_model()
