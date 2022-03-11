from tkinter import *
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import moviepy.video.io.ImageSequenceClip
import moviepy.editor
import numpy
import time
import cv2
import os


def m0_default(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame


class VideoPlayer(ttk.Frame):

    def __init__(self, keys=None, values=None):
        ttk.Frame.__init__(self, None)
        self.master.geometry('1000x700+0+0')
        self.main_panel = Frame(self.master, relief=SUNKEN, bg='black')
        self.main_panel.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)
        self.winfo_toplevel().title('Gesture Recognition')

        icons_store = ['icon_load', 'icon_live', 'icon_pause', 'icon_play', 'icon_record', 'icon_stop', 'icon_off', 'icon_on']
        for i in icons_store:
            img = Image.open(f'icons/{i}.png')
            img = ImageTk.PhotoImage(img)
            setattr(self, f'{i}', img)

        aa = ['button_load_video', 'button_live_video', 'button_control_video', 'button_record_video', 'button_stop_video', 'button_settings_video']
        bb = ['load_video', 'live_video', 'control_video', 'record_video', 'stop_video', 'settings_video']
        cc = [self.icon_load, self.icon_live, self.icon_pause, self.icon_record, self.icon_stop, self.icon_off]
        dd = [self.load_video, self.live_video, self.control_video, self.record_video, self.stop_video, self.settings_video]

        canvas_image = Canvas(self.main_panel, bg='black', highlightthickness=0)
        canvas_image.pack(fill=BOTH, expand=True, side=TOP)
        self.board = Label(canvas_image, bg='black', width=44, height=14)
        self.board.pack(fill=BOTH, expand=True)
        self.set_background()

        canvas_progressbar = Canvas(self.main_panel, relief=FLAT, bg='black', height=2, highlightthickness=0)
        canvas_progressbar.pack(fill=X, padx=0, pady=5)
        self.progressbar = ttk.Progressbar(canvas_progressbar, style='red.Horizontal.TProgressbar', orient='horizontal', length=200, mode='determinate')
        self.progressbar.pack(fill=X, padx=0, pady=5, expand=True)

        control_frame = Frame(self.main_panel, relief=SUNKEN, bg='black')  # control panel
        control_frame.pack(side=BOTTOM, fill=X, padx=10)

        for i in range(6):
            button = Button(control_frame, padx=10, pady=10, bd=8, highlightthickness=0, text=bb[i], font=('arial', 12, 'bold'), fg='#90ee90', bg='black', activeforeground='#90ee90', activebackground='black', image=cc[i], height=40, width=40, command=dd[i])
            button.pack(side='left')
            setattr(self, aa[i], button)

        self.options = {'m0_default': m0_default}
        if keys is not None:
            for i, j in zip(keys, values):
                self.options[i] = j

        self.clicked = StringVar()
        self.clicked.set('m0_default')

        self.method_name = m0_default
        self.button_dropdown = OptionMenu(control_frame, self.clicked, *self.options.keys(), command=self.select_algo)
        self.button_dropdown.configure(padx=10, pady=10, bd=8, highlightthickness=0, text='select_algo', font=('arial', 12, 'bold'), fg='#90ee90', bg='black', activeforeground='#90ee90', activebackground='black')
        self.button_dropdown['menu'].configure(font=('arial', 12, 'bold'), fg='#90ee90', bg='black')
        self.button_dropdown.pack(side='left')

        self.frame_counter = Label(control_frame, padx=10, pady=10, bd=8, highlightthickness=0, font=('arial', 10, 'bold'), fg='#80aaff', bg='black', height=2, width=90)
        self.frame_counter.pack(side='left')

    def load_video(self):
        filetypes = [('All files', '*.*'), ('MP4 files', '*.mp4'), ('MKV files', '*.mkv'), ('AVI files', '*.avi'), ('WMV files', '*.wmv'), ('PNG files', '*.png'), ('JPG files', '*.jpg'), ('JPEG files', '*.jpeg')]
        self.video_filename = filedialog.askopenfilename(title='select a video for recognition', filetypes=filetypes)
        ename = os.path.splitext(self.video_filename)[-1].lower()

        if ename in ['.mp4', '.mkv', '.avi', '.wmv', '.png', '.jpg', '.jpeg']:
            self.winfo_toplevel().title(f'{os.path.basename(self.video_filename)}')
            self.__cap = cv2.VideoCapture(self.video_filename)
            self.frame_number = int(self.__cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.progressbar['maximum'] = self.frame_number
            self.run_frames()

    def live_video(self):
        self.winfo_toplevel().title('camera')
        self.video_filename = 'live_video'
        self.__cap = cv2.VideoCapture(0)
        self.frame_number = 0
        self.run_frames()

    def record_video(self):
        red_hood = self.master.title()
        red_wing = 'live_video' in self.video_filename
        tname = red_hood if red_hood == 'Gesture Recognition' else 'camera [record]' if red_wing else f'{os.path.basename(self.video_filename)} [record]'
        if self.master.title() == tname:
            return

        self.winfo_toplevel().title(tname)
        self.pause_or_play(run=False)

        iname = 'live_video' if red_wing else os.path.basename(self.video_filename).split('.')[0]
        ctime = time.strftime('%Y%m%d%H%M%S', time.gmtime())
        output = f'recognized/{iname}_{ctime}.mp4'

        fps = self.frame_pass / self.counter
        if not red_wing:
            video = moviepy.editor.VideoFileClip(self.video_filename)
            video_duration = int(video.duration)
            fps = self.frame_number / video_duration

        clips = list()
        for frame in self.frame_list:
            frame = numpy.asarray(frame)
            clips.append(frame)

        clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(clips, fps=fps)
        clip.write_videofile(output)

    def control_video(self):
        if not hasattr(self, 'finished') or self.finished:
            return

        self.run = False if not self.__cap.isOpened() else not self.run

        red_wing = 'live_video' in self.video_filename
        red_hood = 'camera' if red_wing else os.path.basename(self.video_filename)
        tname = f'{red_hood} [pause]' if not self.run else f'{red_hood}'
        self.winfo_toplevel().title(tname)

        self.stop_time() if not self.run else self.start_time()
        icon = self.icon_play if not self.run else self.icon_pause
        self.button_control_video.config(image=icon)

    def stop_video(self):
        if not hasattr(self, 'finished') or self.finished:
            return

        self.activate_button(finished=True)
        self.__cap.release()
        cv2.destroyAllWindows()
        self.set_background()

    def settings_video(self):
        self.dragged = False
        self.check = True if not hasattr(self, 'check') else not self.check
        icon = self.icon_on if self.check else self.icon_off
        variable = self.master.bind('<Configure>', self.drag)

        self.button_settings_video.config(image=icon)
        if not self.check:
            self.master.unbind('<Configure>', variable)

    def select_algo(self, _):
        self.method_name = self.options[self.clicked.get()]

    def set_background(self):
        image = ImageTk.PhotoImage(image=Image.open('icons/icon_bsl.png'))
        self.board.image = image
        self.board.config(image=image)

    def update_progress(self):
        text = ''
        elapsed = time.strftime('%H:%M:%S', time.gmtime(self.counter))

        if self.frame_number == 0:
            text = f'FRAME - {self.frame_pass}\t\t\tSECOND - {elapsed}'

        if self.frame_number > 1:
            length = time.strftime('%H:%M:%S', time.gmtime(self.frame_number * self.counter / self.frame_pass))
            percent = int(100 * self.frame_pass / self.frame_number)
            text = f'FRAME - {self.frame_pass} / {self.frame_number} [ {percent}% ]\t\t\tSECOND - {elapsed} / {length}'

        self.frame_counter['text'] = text
        self.progressbar['value'] = self.frame_pass if self.frame_number else 0
        self.progressbar.update()
        if self.frame_pass >= 3600:
            self.stop_video()

    def run_frames(self):
        self.frame_list = list()
        self.frame_pass = 0
        self.counter = 0
        self.activate_button(finished=False)

        while self.__cap.isOpened():
            if self.run:
                ret, frame = self.__cap.read()
                if ret:
                    self.show_image(frame)
                    self.frame_pass += 1
                    self.update_progress()
                else:
                    self.stop_video()
            self.board.update()

    def show_image(self, frame):
        red_wing = self.frame_number == 0 or 'live_video' in self.video_filename
        dimension = (1530, 970) if red_wing else (1530, 730)

        emage = cv2.resize(frame, (1600, 900))
        emage = self.method_name(emage)
        self.frame_list.append(emage)

        image = cv2.resize(emage, dimension)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image=image)
        self.board.config(image=image)
        self.board.image = image

    def drag(self, _):
        self.stop_time()
        self.pause_or_play(run=False)

    def activate_button(self, finished):
        self.finished = finished
        color = 'white' if self.finished else 'black'
        self.button_dropdown['state'] = 'normal' if self.finished else 'disabled'
        self.button_stop_video.configure(bg=color)
        self.pause_or_play(run=not self.finished)

    def pause_or_play(self, run):
        self.run = run
        icon = self.icon_pause if self.run else self.icon_play
        self.button_control_video.config(image=icon)
        self.stop_time() if not self.run else self.start_time()

    def count_time(self):
        if self.running:
            self.counter += 1
            self.master.after(1000, self.count_time)

    def start_time(self):
        self.running = True
        self.count_time()

    def stop_time(self, _=None):
        if _ is not None:
            self.dragged = True
        self.running = False


# https://github.com/orenber/videoPlayer