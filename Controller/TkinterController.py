from tkinter import Entry, StringVar, Label, Button, OptionMenu
from PIL import ImageTk, Image

class TkinterController:
    def return_entry_field(self, placeholder_text, pos, padding, width, callback):
        var = StringVar()
        var.trace("w", lambda name, index, mode, var=var: callback(var))

        entry_field = Entry(text=placeholder_text, textvariable=var)
        entry_field.pack(pady=padding)
        entry_field.config(width=width)
        entry_field.place(x=pos[0], y=pos[1])

        return entry_field

    def place_image(self, gui, image_path, posx, posy, size=None):
        card_image = Image.open(image_path)
        if not size is None:
            card_image = card_image.resize((size))
        render = ImageTk.PhotoImage(card_image)

        label = Label(gui, image=render)
        label.image = render
        label.place(x=posx, y=posy)

    def add_button(self, gui, text, callback_command, pady, width, posx, posy):
        button = Button(gui, text=text, command=callback_command)
        button.pack(pady=pady)
        button.config(width=width)
        button.place(x=posx, y=posy)
        return button

    def add_card_button(self, gui, text, callback_command, pady, width, posx, posy, card, section, max_in_section):
        button = Button(gui, text=text, command=lambda: callback_command(card, section, max_in_section))
        button.pack(pady=pady)
        button.config(width=width)
        button.place(x=posx, y=posy)
        return button

    def add_dropdown(self, gui, options, pady, width, posx, posy, callback):
        variable = StringVar(gui)
        variable.set(options[0])
        variable.trace("w", lambda name, index, mode, var=variable: callback(var))

        options_menu = OptionMenu(gui, variable, *options)
        options_menu.pack(pady=pady)
        options_menu.place(x=posx, y=posy)
        options_menu.config(width=width)
        return options_menu


    def clear_gui(self, gui):
        for widget in gui.winfo_children():
            widget.destroy()