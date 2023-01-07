import logging as logging
from datetime import datetime

import os

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import tkinter.colorchooser as colorchooser

import PIL as pil
import json

def createLogger(type = 'console'):
    format = '%(asctime)s %(levelname)s:%(message)s'
    datefmt = '%I:%M:%S %p'
    level = logging.DEBUG

    filename = f'logs/{datetime.now().strftime("%m-%d-%y_%H-%M-%S")}.log'

    if type == 'file':
        try:
            os.mkdir('logs')
        except:
            pass

        logging.basicConfig(filename=filename, filemode='w', format=format, datefmt=datefmt, level=level)
    else:
        logging.basicConfig(format=format, datefmt=datefmt, level=level)

createLogger()
# createLogger('file')

class Window(tk.Tk):
    def __init__(this, *args, **kwargs):
        super().__init__(*args, **kwargs)
        this.title('')
        this.geometry('%dx%d' % (760 , 610) )
        this.minsize(700, 300)

        this.panedwindow = ttk.PanedWindow(orient='horizontal')
        this.panedwindow.pack(fill='both', expand=True)

        this.optionsframe = ttk.LabelFrame(this.panedwindow, text='Options', width=250)
        this.mainframe = ttk.Frame(this.panedwindow, borderwidth=2)

        this.panedwindow.add(this.optionsframe)
        this.panedwindow.add(this.mainframe)

        this.animations = []
        this.settings = {}
        this.settingsFile = 'settings.json'
        this.loadSettings()

        this.createMenuBar()

        this.initialize()

    def initialize(this):
        this.isnumber = (this.register(this.checkNumber), '%S', '%d')
        this.isint = this.register(lambda *args: this.checkNumber(*args, exclude=['-', '.']))
        this.createCanvas()
        this.createOptionsBar()
        this.createOptionsTab()
    
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

    def createOptionsTab(this):
        # entry = ttk.Entry(this.optionsframe, validate='all', validatecommand=lambda args: print(args))
        # entry.pack()
        pass

    def checkNumber(this, value = None, action = None, include = [], exclude = [], callback = None):
            """
            value = %S
            action = %d
            """

            logging.info(f'{value}, {action}')

            # result = False

            # if int(action) < 1 and action != None:
            #     result = True

            result = ((value in ['-', '.'] or value in include) or str(value).isnumeric()) and not value in exclude

            logging.info(result)
            return result
    
    

    def createOptionsBar(this):

        this.optionsBar = ttk.Frame(this.mainframe)

        entryWidth = 5
        
        this.optionsWidgets = {
            'x_spacing': {
                'label': ttk.Label(this.optionsBar, text='X Spacing'),
                'var': tk.IntVar(),
            },
            'y_spacing': {
                'label': ttk.Label(this.optionsBar, text='Y Spacing'),
                'var': tk.IntVar(),
            },
            'width': {
                'label': ttk.Label(this.optionsBar, text='Sheet Width'),
                'var': tk.IntVar(),
            },
            'auto_width': {
                'var': tk.BooleanVar(),
            },
        }

        this.optionsWidgets['x_spacing']['spinbox'] = ttk.Spinbox(this.optionsBar, textvariable=this.optionsWidgets['x_spacing']['var'], width=entryWidth, validate='key', validatecommand=(this.isint, '%S', '%d'), from_=0, to=999)
        this.optionsWidgets['y_spacing']['spinbox'] = ttk.Spinbox(this.optionsBar, textvariable=this.optionsWidgets['y_spacing']['var'], width=entryWidth, validate='key', validatecommand=(this.isint, '%S', '%d'), from_=0, to=999)
        this.optionsWidgets['width']['spinbox'] = ttk.Spinbox(this.optionsBar, textvariable=this.optionsWidgets['width']['var'], width=entryWidth, validate='key', validatecommand=(this.isint, '%S', '%d'), from_=0, to=999)
        this.optionsWidgets['auto_width']['checkbox'] = ttk.Checkbutton(this.optionsBar, text='Minimize Width', variable=this.optionsWidgets['auto_width']['var'], onvalue=True, offvalue=False, command=this.updateSettings)

        this.optionsWidgets['x_spacing']['var'].set(this.settings['x_spacing'])
        this.optionsWidgets['y_spacing']['var'].set(this.settings['y_spacing'])
        this.optionsWidgets['width']['var'].set(this.settings['width'])
        this.optionsWidgets['auto_width']['var'].set(int(this.settings['auto_width']))
        
        this.optionsWidgets['x_spacing']['var'].trace("w", lambda name, index, mode: this.updateSettings() )
        this.optionsWidgets['y_spacing']['var'].trace("w", lambda name, index, mode: this.updateSettings() )
        this.optionsWidgets['width']['var'].trace("w", lambda name, index, mode: this.updateSettings() )
        this.optionsWidgets['auto_width']['var'].trace("w", lambda name, index, mode: this.updateSettings() )

        this.optionsWidgets['auto_width']['checkbox'].pack(side='right', padx=2)

        this.optionsWidgets['width']['spinbox'].pack(side='right', padx=2)
        this.optionsWidgets['width']['label'].pack(side='right', padx=2)

        this.optionsWidgets['y_spacing']['spinbox'].pack(side='right', padx=2)
        this.optionsWidgets['y_spacing']['label'].pack(side='right', padx=2)

        this.optionsWidgets['x_spacing']['spinbox'].pack(side='right', padx=2)
        this.optionsWidgets['x_spacing']['label'].pack(side='right', padx=2)



        this.optionsBar.pack( fill='x')

    def updateSettings(this):
        this.settings['x_spacing'] = this.optionsWidgets['x_spacing']['var'].get()
        this.settings['y_spacing'] = this.optionsWidgets['y_spacing']['var'].get()
        this.settings['width'] =this.optionsWidgets['width']['var'].get()
        this.settings['auto_width'] = this.optionsWidgets['auto_width']['var'].get()

        logging.info(this.settings)

        this.saveSettings()

    # settings
    def loadSettings(this, **kwargs):
        try:
            this.settings = kwargs['settings']
        except:
            try:
                with open(this.settingsFile, 'r') as file:
                    this.settings = json.load(file)

                logging.info(this.settings)
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