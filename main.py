import tkinter as tk
from tkinter import colorchooser
import PyPDF2
import threading
import time

class PDFWordDisplay:
    def __init__(self, root, file_path):
        self.root = root
        self.is_fullscreen = True
        self.root.attributes('-fullscreen', self.is_fullscreen)
        self.root.configure(bg='black')
        
        self.font_size = 48
        self.label = tk.Label(root, text='', fg='white', bg='black', font=('Helvetica', self.font_size))
        self.label.pack(expand=True)

        self.page_label = tk.Label(root, text='', fg='white', bg='black', font=('Helvetica', 24))
        self.page_label.place(relx=1.0, rely=0.0, anchor='ne')

        self.words, self.pages = self.pdf_to_words(file_path)
        self.word_index = 0
        self.delay = 0.5
        self.running = False

        self.create_controls()
        self.create_color_controls()
        self.create_page_controls()
        self.update_display()

    def pdf_to_words(self, file_path):
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            words = []
            pages = []
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                page_words = text.split()
                words.extend(page_words)
                pages.extend([page_num + 1] * len(page_words))
        return words, pages

    def create_controls(self):
        control_frame = tk.Frame(self.root, bg='black')
        control_frame.pack()

        self.play_button = tk.Button(control_frame, text="Play", command=self.play, bg='white', font=('Helvetica', 24))
        self.play_button.pack(side='left')

        self.pause_button = tk.Button(control_frame, text="Pause", command=self.pause, bg='white', font=('Helvetica', 24))
        self.pause_button.pack(side='left')

        self.prev_button = tk.Button(control_frame, text="<<", command=self.prev_word, bg='white', font=('Helvetica', 24))
        self.prev_button.pack(side='left')

        self.next_button = tk.Button(control_frame, text=">>", command=self.next_word, bg='white', font=('Helvetica', 24))
        self.next_button.pack(side='left')

        self.speed_up_button = tk.Button(control_frame, text="Speed Up", command=self.speed_up, bg='white', font=('Helvetica', 24))
        self.speed_up_button.pack(side='left')

        self.slow_down_button = tk.Button(control_frame, text="Slow Down", command=self.slow_down, bg='white', font=('Helvetica', 24))
        self.slow_down_button.pack(side='left')

        self.increase_font_button = tk.Button(control_frame, text="A+", command=self.increase_font, bg='white', font=('Helvetica', 24))
        self.increase_font_button.pack(side='left')

        self.decrease_font_button = tk.Button(control_frame, text="A-", command=self.decrease_font, bg='white', font=('Helvetica', 24))
        self.decrease_font_button.pack(side='left')

        self.exit_button = tk.Button(control_frame, text="Exit", command=self.exit_app, bg='white', font=('Helvetica', 24))
        self.exit_button.pack(side='left')

        self.toggle_fullscreen_button = tk.Button(control_frame, text="Toggle Fullscreen", command=self.toggle_fullscreen, bg='white', font=('Helvetica', 24))
        self.toggle_fullscreen_button.pack(side='left')

    def create_color_controls(self):
        color_control_frame = tk.Frame(self.root, bg='black')
        color_control_frame.place(relx=0.0, rely=0.0, anchor='nw')

        self.change_bg_color_button = tk.Button(color_control_frame, text="Change BG Color", command=self.change_bg_color, bg='white', font=('Helvetica', 12))
        self.change_bg_color_button.pack(side='top')

        self.change_fg_color_button = tk.Button(color_control_frame, text="Change Text Color", command=self.change_fg_color, bg='white', font=('Helvetica', 12))
        self.change_fg_color_button.pack(side='top')

    def create_page_controls(self):
        page_control_frame = tk.Frame(self.root, bg='black')
        page_control_frame.pack(side='bottom')

        self.prev_page_button = tk.Button(page_control_frame, text="<< Page", command=self.prev_page, bg='white', font=('Helvetica', 24))
        self.prev_page_button.pack(side='left')

        self.next_page_button = tk.Button(page_control_frame, text="Page >>", command=self.next_page, bg='white', font=('Helvetica', 24))
        self.next_page_button.pack(side='left')

    def play(self):
        if not self.running:
            self.running = True
            threading.Thread(target=self.display_words).start()

    def pause(self):
        self.running = False

    def prev_word(self):
        if self.word_index > 0:
            self.word_index -= 1
            self.update_display()

    def next_word(self):
        if self.word_index < len(self.words) - 1:
            self.word_index += 1
            self.update_display()

    def speed_up(self):
        if self.delay > 0.1:
            self.delay -= 0.1

    def slow_down(self):
        self.delay += 0.1

    def increase_font(self):
        self.font_size += 4
        self.label.config(font=('Helvetica', self.font_size))

    def decrease_font(self):
        if self.font_size > 8:
            self.font_size -= 4
            self.label.config(font=('Helvetica', self.font_size))

    def prev_page(self):
        current_page = self.pages[self.word_index]
        while self.word_index > 0 and self.pages[self.word_index] == current_page:
            self.word_index -= 1
        self.update_display()

    def next_page(self):
        current_page = self.pages[self.word_index]
        while self.word_index < len(self.words) - 1 and self.pages[self.word_index] == current_page:
            self.word_index += 1
        self.update_display()

    def display_words(self):
        while self.running and self.word_index < len(self.words):
            self.update_display()
            self.word_index += 1
            time.sleep(self.delay)
            self.root.update()

    def update_display(self):
        if 0 <= self.word_index < len(self.words):
            word = self.words[self.word_index]
            page = self.pages[self.word_index]
            self.label.config(text=word)
            self.page_label.config(text=f"Sayfa: {page}")

    def change_bg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.root.configure(bg=color)
            self.label.configure(bg=color)
            self.page_label.configure(bg=color)

    def change_fg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.label.configure(fg=color)
            self.page_label.configure(fg=color)

    def exit_app(self):
        self.root.quit()

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes('-fullscreen', self.is_fullscreen)

if __name__ == '__main__':
    file_path = r'C:\Users\yunus\OneDrive\Masaüstü\hızlı okuma kodu\Henri-Charriere-Kelebek.pdf'
    
    root = tk.Tk()
    app = PDFWordDisplay(root, file_path)
    root.mainloop()