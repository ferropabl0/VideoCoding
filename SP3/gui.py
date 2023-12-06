import os
from tkinter import *
from PIL import Image, ImageTk
import imageio


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
        self.options_label = Label(root, text="Processing Methods")
        self.options_label.pack()

        # Scale factor for video frames
        self.scale_factor = 0.33
        self.video_playing = False
        self.video = None

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

    def display_media(self, media_path):
        try:
            if media_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
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
                # Display video
                self.play_video(media_path)
        except Exception as e:
            print(f"Error displaying media: {e}")

    def play_video(self, video_path):
        try:
            self.video_playing = True
            self.video = imageio.get_reader(video_path)

            for frame in self.video.iter_data():
                # Convert each video frame to an ImageTk.PhotoImage
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

    def stop_video(self):
        if self.video:
            self.video_playing = False
            self.video.close()


if __name__ == "__main__":
    root1 = Tk()
    app = ImageProcessorApp(root1)
    root1.mainloop()
