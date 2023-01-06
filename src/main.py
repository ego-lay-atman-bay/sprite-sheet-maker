import os

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import tkinter.colorchooser as colorchooser

import PIL as pil
import json

class Window(tk.Tk):
    def __init__(this, *args, **kwargs):
        super().__init__(*args, **kwargs)
        this.title('')
        this.geometry('%dx%d' % (760 , 610) )

        this.panedwindow = ttk.PanedWindow(orient='horizontal')
        this.panedwindow.pack(fill='both', expand=True)

        this.optionsframe = ttk.LabelFrame(this.panedwindow, text='Options', width=250)
        this.mainframe = ttk.Frame(this.panedwindow, borderwidth=2, width=500)

        this.panedwindow.add(this.optionsframe)
        this.panedwindow.add(this.mainframe)

        this.animations = []
        this.settings = {}
        this.settingsFile = 'settings.json'
        this.loadSettings()

        this.createMenuBar()

        this.initialize()

    def createMenuBar(this):
        this.menuBar = tk.Menu(this)
        this.config(menu=this.menuBar)

        this.fileMenu = tk.Menu(this.menuBar, tearoff=0)
        this.fileMenu.add_command(label= 'New sheet')
        this.fileMenu.add_command(label= 'Open...')
        this.fileMenu.add_separator()
        this.fileMenu.add_command(label='Save')
        this.fileMenu.add_command(label='Save as...')

        this.menuBar.add_cascade(label= 'File', menu=this.fileMenu)


    def initialize(this):
        this.isnumber = (this.register(this.checkNumber), '%5', '%d')
        this.createCanvas()
        this.createOptionsBar()

    def createCanvas(this):
        this.canvas = tk.Canvas(this.mainframe, background='white')
        this.canvas.pack(fill='both', expand=True)

        this.canvasScrollbars = {
            'horizontal': ttk.Scrollbar(this.canvas, orient='horizontal', command=this.canvas.xview),
            'vertical': ttk.Scrollbar(this.canvas, orient='vertical', command=this.canvas.xview)
        }

        this.canvasScrollbars['horizontal'].pack(fill='x', side='bottom')
        this.canvasScrollbars['vertical'].pack(fill='y', side='right')

        this.canvas.config(xscrollcommand=this.canvasScrollbars['horizontal'].set)
        this.canvas.config(yscrollcommand=this.canvasScrollbars['vertical'].set)

        this.canvas.bind('<MouseWheel>', lambda e: this.canvasScroll((0, e.delta/120)))
        this.canvas.bind('<Shift-MouseWheel>', lambda e: this.canvasScroll((e.delta/120, 0)))
    
    def canvasScroll(this, amount: tuple):
        this.canvas.xview_scroll(int(-1*amount[0]), 'units')
        this.canvas.yview_scroll(int(-1*amount[1]), 'units')

    def updateCanvasScroll(this):
        xlist = []
        ylist = []
        for obj in this.animations:
            x,y = this.canvas.coords(obj['image'])
            xlist.append(x)
            ylist.append(y)

        minX = min([0] + xlist)
        minY = min([0] + ylist)
        maxX = max([this.size[0]] + xlist)
        maxY = max([this.size[1]] + ylist)
        this.canvas.config(scrollregion=(minX - 200, minY - 200, maxX + 200, maxY + 200))

    def checkNumber(this, value = None, action = None):
            """
            value = %5
            action = %d
            """

            print(value, action)

            result = False

            # if int(action) < 1 and action != None:
            #     result = True

            result = value in ['-', '.'] or str(value).isnumeric()

            print(result)
            return result
    
    

    def createOptionsBar(this):

        this.optionsBar = ttk.Frame(this.mainframe)
        
        this.optionsWidgets = {
            'x_spacing': {
                'label': ttk.Label(this.optionsBar, text='X Spacing'),
                'spinbox': ttk.Spinbox(this.optionsBar, width=10, validate='key', validatecommand=this.isnumber)
            }
        }
        this.optionsWidgets['x_spacing']['spinbox'].pack(side='right', padx=2)
        this.optionsWidgets['x_spacing']['label'].pack(side='right', padx=2)

        this.optionsBar.pack(side='bottom', fill='x')

    # settings
    def loadSettings(this, **kwargs):
        try:
            this.settings = kwargs['settings']
        except:
            try:
                with open(this.settingsFile, 'r') as file:
                    this.settings = json.load(file)

                print(this.settings)
            except:
                this.initSettings()
                this.saveSettings()
        
    def initSettings(this):
        this.settings = {
            'x_spacing': 2,
            'y_spacing': 2,
            'width': 100,
            'auto_width': False,
        }

    def saveSettings(this):
        file = open(this.settingsFile, 'w+')
        json.dump(this.settings, file, indent=2)


def main():
    app = Window()
    app.mainloop()

if __name__ == '__main__':
    main()