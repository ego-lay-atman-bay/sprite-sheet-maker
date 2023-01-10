import tkinter as tk
import tkinter.ttk as ttk
from tkcolorpicker import askcolor

from PIL import Image, ImageTk, ImageColor
    
class ColorPicker(ttk.Button):
    def __init__(this, *args, color : str = 'white', alpha = False, size : int = 15, texvariable = None, command = None, **kwargs):
        super().__init__(*args, **kwargs)
        
        this.textvariable = texvariable
        
        this.size = size
        
        this.alpha = alpha
        this.color = color
        this.rgba = this.getColor(color)
        
        this.setColor(this.color)
        this.command = command
        
        this.configure(command=this.pickColor)
        
    def getColor(this, color):
        if color == 'transparent':
            return (0, 0, 0, 255)
        else:
            return ImageColor.getcolor(color, 'RGBA')
        
    def setColor(this, color : str = None):
        if color != None:
            this.color = color
            this.rgba = this.getColor(color)
            
        if this.textvariable:
            this.textvariable.set(this.color)
            
        this._image = Image.new('RGBA', (this.size, this.size), color=this.rgba)
        this._photoimage = ImageTk.PhotoImage(this._image)
        
        this.configure(image=this._photoimage)
        
    def pickColor(this):
        color = askcolor(this.getColor(this.color), this, alpha=this.alpha)
        if color[1] != None:
            this.rgba, this.color = color
            this.setColor()
            
        if callable(this.command):
            this.command()
        
        # print(this.color)
        
        return this.color
        
        
if __name__ == "__main__":
    
    root = tk.Tk()
    # style = ttk.Style(root)
    # style.theme_use('clam')

    var = tk.StringVar()

    picker = ColorPicker(root, color='yellow', alpha=True, texvariable=var, command=lambda : print('test'))

    var.trace('w', lambda name, index, mode: print(var.get()))
    picker.pack()

    root.mainloop()