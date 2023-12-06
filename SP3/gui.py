import os
from tkinter import *
from PIL import Image, ImageTk
import imageio
import cv2


class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image and Video Processor")

        # Image listbox
        self.image_listbox = Listbox(root, selectmode=SINGLE)
        self.image_listbox.pack(side=LEFT, fill=Y)
        self.image_listbox.bind('<<ListboxSelect>>', self.load_media)
        self.load_media_in_folder()

        # Canvas for media display
        self.canvas_width = 600  # Set the initial canvas width
        self.canvas_height = 400  # Set the initial canvas height
        self.canvas = Canvas(self.root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        # Options label
        self.options_label = Label(root, text="Tools")
        self.options_label.pack()

        # Scale factor for video frames
        self.scale_factor = 0.33
        self.video_playing = False
        self.video = None

        self.play_button = Button(root, text="Play", command=self.play_video2)
        self.play_button.pack(side=LEFT)

        self.pause_button = Button(root, text="Pause", command=self.pause_video)
        self.pause_button.pack(side=LEFT)

        self.bw_button = Button(root, text="Black & White", command=self.convert_to_black_and_white)
        self.bw_button.pack(side=LEFT)

    def load_media_in_folder(self):
        files = [f for f in os.listdir('.') if
                 f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.mp4', '.avi', '.mkv', '.mov'))]
        for file in files:
            self.image_listbox.insert(END, file)

    def load_media(self, event):
        selected_index = self.image_listbox.curselection()
        if selected_index:
            selected_file = self.image_listbox.get(selected_index[0])
            media_path = os.path.join('.', selected_file)

            if self.video_playing:
                self.stop_video()
            self.canvas.delete("all")
            self.display_media(media_path)
            self.media_path = media_path
            self.bw_vid_button = Button(self.root, text="Black & White", command=self.play_bw_video(media_path))
            self.bw_vid_button.pack(side=LEFT)

    def display_media(self, media_path):
        try:
            if media_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                self.bw_button.pack(side=LEFT)
                self.bw_vid_button.pack_forget()
                # Display image
                image = Image.open(media_path)
                image.thumbnail((300, 300))

                photo = ImageTk.PhotoImage(image)
                x = (self.canvas_width - photo.width()) // 2
                y = (self.canvas_height - photo.height()) // 2

                self.canvas.config(width=self.canvas_width, height=self.canvas_height)
                self.canvas.create_image(x, y, anchor=NW, image=photo)
                self.canvas.image = photo

            elif media_path.lower().endswith(('.mp4', '.avi', '.mkv', '.mpg')):
                self.bw_button.pack_forget()
                self.bw_vid_button.pack(side=LEFT)
                self.play_video(media_path)

        except Exception as e:
            print(f"Error displaying media: {e}")

    def play_video(self, video_path):
        try:
            self.video_playing = True
            self.video = imageio.get_reader(video_path)
            self.bw_button.pack_forget()
            for frame in self.video.iter_data():
                if not self.video_playing:
                    break  # Stop if the user clicks the stop button

                scaled_frame = Image.fromarray(frame)
                scaled_frame = scaled_frame.resize((int(scaled_frame.width * self.scale_factor),
                                                    int(scaled_frame.height * self.scale_factor)))
                photo = ImageTk.PhotoImage(scaled_frame)

                x = (self.canvas_width - photo.width()) // 2
                y = (self.canvas_height - photo.height()) // 2

                self.canvas.config(width=self.canvas_width, height=self.canvas_height)
                self.canvas.create_image(x, y, anchor=NW, image=photo)
                self.canvas.image = photo
                self.root.update()
        except Exception as e:
            print(f"Error playing video: {e}")

    def play_bw_video(self, video_path):
        try:
            self.video_playing = True
            self.video = imageio.get_reader(video_path)

            self.bw_button.pack_forget()

            for frame in self.video.iter_data():
                if not self.video_playing:
                    break  # Stop if the user clicks the stop button

                # Convert the frame to black and white
                bw_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                scaled_frame = Image.fromarray(bw_frame)
                scaled_frame = scaled_frame.resize((int(scaled_frame.width * self.scale_factor),
                                                    int(scaled_frame.height * self.scale_factor)))
                photo = ImageTk.PhotoImage(scaled_frame)

                x = (self.canvas_width - photo.width()) // 2
                y = (self.canvas_height - photo.height()) // 2

                self.canvas.config(width=self.canvas_width, height=self.canvas_height)
                self.canvas.create_image(x, y, anchor=NW, image=photo)
                self.canvas.image = photo
                self.root.update()
        except Exception as e:
            print(f"Error playing video: {e}")

    def convert_to_black_and_white(self):
        selected_index = self.image_listbox.curselection()
        if selected_index:
            selected_file = self.image_listbox.get(selected_index[0])
            media_path = os.path.join('.', selected_file)

            try:
                image = Image.open(media_path)
                image = image.convert("L")  # Convert to grayscale (black and white)
                image.thumbnail((300, 300))

                photo = ImageTk.PhotoImage(image)
                x = (self.canvas_width - photo.width()) // 2
                y = (self.canvas_height - photo.height()) // 2

                self.canvas.config(width=self.canvas_width, height=self.canvas_height)
                self.canvas.create_image(x, y, anchor=NW, image=photo)
                self.canvas.image = photo

            except Exception as e:
                print(f"Error converting to black and white: {e}")

    def pause_video(self):
        self.video_playing = False

    def play_video2(self):
        self.play_video(self.media_path)

    def stop_video(self):
        if self.video:
            self.video_playing = False
            self.video.close()


if __name__ == "__main__":
    root1 = Tk()
    app = ImageProcessorApp(root1)
    root1.mainloop()
