import json, os, re, time
from enum import Enum
from time import sleep
from tkinter import (BooleanVar, Canvas, DoubleVar, IntVar, StringVar, Tk,
                     colorchooser)
from tkinter.ttk import *
from types import *
from warnings import warn

import ttkthemes
from _tkinter import TclError
from Cope import darken, debug, debugged, reprise, rgbToHex
from ScrolledFrame import ScrolledFrame
from TkOptionMenu import OptionsMenu
from TkOptions import Option, getOptions
from Tooltip import Tooltip

from os.path import dirname; DIR = dirname(__file__)

#* Include any files from which you want to get globals from here



SCROLL_SPEED = 1
SCREEN_WIDTH_DIVISOR  = 1.1
SCREEN_HEIGHT_DIVISOR = 1.1

RESET_FILE = False

SETTINGS_FILE = DIR + '/settings.json'
FUNC_TYPES = (FunctionType, BuiltinFunctionType, BuiltinMethodType, LambdaType, MethodWrapperType, MethodType)



globalsDict = globals()
def getOptions(obj=None, namespace=None):
    ''' Gets all the Option members in the passed in class. The passed in class must have a default constructor. '''
    global globalsDict

    if obj is None:
        if namespace is None:
            options = [globalsDict[attr] for attr in globalsDict if not callable(globalsDict[attr]) and not attr.startswith("__") and type(globalsDict[attr]) == Option]
        else:
            options = [namespace[attr] for attr in namespace if not callable(namespace[attr]) and not attr.startswith("__") and type(namespace[attr]) == Option]
    else:
        options = [getattr(obj, attr) for attr in dir(obj) if not callable(getattr(obj, attr)) and not attr.startswith("__") and type(getattr(obj, attr)) == Option]
    return options



namespace = globals()
def createOptionMenu(*instances, getGlobal=True, windowName='Options', sort=True, nonBlocking=False, styleOptionTab='General', **names):
    options = []

    #* Go through the classes passed in, get all the options from them, and add them to members under their key (and sort them)
    for i in instances:
        options += getOptions(i)

    #* Do the same with global variables
    if getGlobal:
        options += getOptions(namespace=namespace)

    if sort:
        options.sort()

    OptionsMenu(Tk(className=windowName), *options, styleOptionTab=styleOptionTab).mainloop()

    # Escape debouncing
    sleep(.15)



def generateStyle():
    s = ttkthemes.ThemedStyle()
    # s.theme_use('default')

    # bg = rgbToHex((49, 54, 59))
    bg = '#31363b'
    fg = rgbToHex((200, 200, 200))

    s.configure('.',         background=bg)
    s.configure('TLabel',    foreground=fg)
    s.configure('TFrame',    background=bg)
    s.configure('TCombobox', fieldbackground=bg)
    s.configure('TEntry',    fieldbackground=bg)
    s.configure('TSpinbox',  fieldbackground=bg)
    s.configure('TButton',   foreground=fg)

    return s



# http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame
class ScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, parent, backgroundColor=(49, 54, 59), *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        #* Create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient='vertical')
        vscrollbar.pack(fill='y', side='right', expand=0)
        # parent.grid_rowconfigure(0, weight=8)
        # parent.grid_rowconfigure(1, weight=8)
        # parent.grid_rowconfigure(2, weight=8)

        # vscrollbar.grid(column=10, row=0, rowspan=200, sticky='E')
        self.canvas = Canvas(self, bd=False, highlightthickness=0, yscrollcommand=vscrollbar.set, bg=rgbToHex(backgroundColor))
        self.canvas.pack(side='top', fill='both', expand=1)
        # self.canvas.grid() #row=0, column=0, rowspan=20, columnspan=20)
        vscrollbar.config(command=self.canvas.yview)

        #* Reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        #* create a frame inside the canvas which will be scrolled with it
        self.scrolledFrame = scrolledFrame = Frame(self.canvas)
        interior_id = self.canvas.create_window(0, 0, window=scrolledFrame, anchor='nw')


        #* Track changes to the canvas and frame width and sync them,
        #   also updating the scrollbar
        def _configure_interior(event):
            #* update the scrollbars to match the size of the inner frame
            size = (scrolledFrame.winfo_reqwidth(), scrolledFrame.winfo_reqheight())
            self.canvas.config(scrollregion="0 0 %s %s" % size)
            if scrolledFrame.winfo_reqwidth() != self.canvas.winfo_width():
                #* update the canvas's width to fit the inner frame
                self.canvas.config(width=scrolledFrame.winfo_reqwidth())
        scrolledFrame.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if scrolledFrame.winfo_reqwidth() != self.canvas.winfo_width():
                #* update the inner frame's width to fill the canvas
                self.canvas.itemconfigure(interior_id, width=self.canvas.winfo_width())
        self.canvas.bind('<Configure>', _configure_canvas)



@reprise
class Option:
    """
        A class that automatically handles options for you.

                  title
               ____________
        label [ widgetText ]
               ------------

        Params:
            value: The default value of the option. The type of
                element created will be automatically determined
                based on the type of this parameter, unless
                explicitly overwritten by the type_ parameter.
                Will get overwritten by the value in settings.json
            label: The text to the left of the element
            tab: The tab the option goes under
            widgetText: The text that goes on the element, if applicable
            title: The text that goes above the element
            currentItem: The default selected item in a drop-down box.
                Will get overwritten by the value in settings.json.
            tooltip: The text that appears magically when the element
                is hovered over
            min/max: The minimum and maximum values a spinbox will allow.
            var: The name of the variable this is assigned to. (if specified,
                it appears at the bottom of the tooltip in parenthesis)
            type_: Manually specify the type of element to use.
                NOTE: When making a color Option, this must be 'Color'.
                NOTE: When making a stationary label element, the value param
                    should be a tk.StringVar, or this should be specified as
                    'Label' or 'Tracker'
            updateFunc: A function that is called when an option is changed
                in some way. DO NOT USE THIS WITH A BUTTON OR A COLOR
            params/kwparams: A LIST and DICT (Not starred!) of parameters
                passed into the function call, if the element is a button
                or updateFunc is specified.


        Notes:
            To access the Option, you must use the get() and set() functions.
            The ~ (invert) operator is also overloaded to be equivelent to the
            get() function for easy access, but may cause occasional issues.

    """
    order = [bool, Enum, list, tuple, set, str, float, int, 'color', *FUNC_TYPES, *LABEL_TYPES]

    def __init__(self, value, label='', tab='General', widgetText='', title='', currentItem=None, tooltip='',
                 min=None, max=None, var='', type_=None, updateFunc=lambda value, *a, **kw: None, params=(), kwparams={}):
        self.defaultValue = value
        self.type = type_
        self.tab = tab
        self.title = title
        self.updateFunc = updateFunc
        self.params = params
        self.kwparams = kwparams

        #* Add the (variable) to the end of the tooltip
        if var is not None:
            tooltip +=  f'\n({var})' if len(tooltip) else ''

        if type(self.type) is str:
            self.type = self.type.lower()

        validTypeList = self.order


        #* If value is an Enum
        if type(value) not in validTypeList and issubclass(value, Enum) and type_ is None:
            self.enum = value
            self.type = list
            self.options = [var for var, member in value.__members__.items()]
            if currentItem is not None:
                try:
                    self.value = currentItem.name
                    self.defaultValue = self.value
                except AttributeError:
                    raise UserWarning("The value given to the option is not in the enum provided.")
        else:
            self.enum = None
            self.value = value
            if type_ is None:
                self.type = type(value)

            if self.type in (list, tuple, set):
                self.options = value
                self.value = currentItem

            elif self.type is StringVar:
                self.value = value.get()
                self._value = value

        if self.type not in validTypeList:
            raise TypeError(f"The Option class only supports ints, float, bools, tuples, lists, enums, and strings, not {self.type}")

        self.min = min
        if self.min is None:
            if self.type in (int, float):
                self.min = 0

        self.max = max
        if self.max is None:
            if self.type in (int, float):
                self.max = 100000

        if self.value is None:
            if self.type in (tuple, list, set):
                self.value = self.value[0]

        self.element = None
        if not len(label) and not len(widgetText) and not len(tooltip) and not len(title) and not len(var):
            raise UserWarning('This option has no labels!')
        self.saveName = var if len(var) else label if len(label) else widgetText if len(widgetText) else title if len(title) else tooltip
        self.label = label
        self._value = None
        self.widgetText = widgetText
        self.tooltip = tooltip

        if self.type in FUNC_TYPES:
            self.func = value
            # self.func = lambda self: self.returnVal = value(*self.params, **self.kwparams)
            self.value = None
            self.defaultValue = None

        if RESET_FILE:
            self.restoreDefault()

        #* Load the value from the settings file over the given default value
        if not os.path.exists(SETTINGS_FILE):
            os.system('touch ' + SETTINGS_FILE)
            with open(SETTINGS_FILE, 'r+') as f:
                json.dump({}, f)

            self.restoreDefault()
        else:
            # If we have just added a new option in code, it will throw an error. Catch that error, restore to defaults, and try again
            try:
                with open(SETTINGS_FILE, 'r+') as f:
                    self.value = json.load(f)[self.saveName]
            except KeyError:
                self.restoreDefault()
                with open(SETTINGS_FILE, 'r+') as f:
                    self.value = json.load(f)[self.saveName]

    def callback(self):
        self._value = self.func(*self.params, **self.kwparams)

    def restoreDefault(self):
        print(f'Reseting {self.value} to {self.defaultValue}')
        self.value = self.defaultValue
        if self._value is not None and self.type != 'color':
            self._value.set(self.defaultValue)
        elif self.type =='color':
            self._value = self.defaultValue

        try:
            with open(SETTINGS_FILE, "r") as jsonFile:
                data = json.load(jsonFile)
        except json.decoder.JSONDecodeError:
            with open(SETTINGS_FILE, "w") as jsonFile:
                json.dump({}, jsonFile)
            with open(SETTINGS_FILE, "r") as jsonFile:
                data = json.load(jsonFile)

        data[self.saveName] = self.defaultValue

        with open(SETTINGS_FILE, "w") as jsonFile:
            json.dump(data, jsonFile)

    def create(self, root):
        if self.type == int:
            self._value = IntVar(root, self.value)
        elif self.type == bool:
            self._value = BooleanVar(root, self.value)
        elif self.type == float:
            self._value = DoubleVar(root, self.value)
        elif self.type in (str, tuple, list, set, 'label', 'tracker'):
            self._value = StringVar(root, self.value)
        elif self.type == 'color':
            self._value = self.value

        if len(self.title):
            title = Label(root, text=self.title)
        else:
            title = None
        if len(self.label):
            label = Label(root, text=self.label)
        else:
            label = None


        if self.type is int:
            self.element = Spinbox(root, from_=self.min, to=self.max, textvariable=self._value)

        elif self.type is float:
            self.element = Entry(root, textvariable=self._value)

        elif self.type is bool:
            self.element = Checkbutton(root, text=self.widgetText, variable=self._value)

        elif self.type is str:
            self.element = Entry(root, text=self.widgetText, textvariable=self._value, exportselection=False)

        elif self.type in (tuple, list, set):
            # print(self._value)
            self.element = Combobox(root, values=self.options, textvariable=self._value)
            # debug(self.value, self.options)
            self.element.current(self.options.index(self.value))
            # self.element.current(0)
            # print(self.element.get())

        elif self.type == 'color':
            self.buttonColor = Style(root)
            self.buttonColor.configure(f'{self.saveName}.TButton', background=rgbToHex(self.value), focuscolor='maroon')#rgbToHex(darken(self.value, 20)))
            self.element = Button(root, command=self.colorPicker, text=self.widgetText, style=f'{self.saveName}.TButton')

        elif self.type in FUNC_TYPES:
            self.element = Button(root, command=self.callback, text=self.widgetText)

        elif self.type in LABEL_TYPES:
            self._value.trace_add('write', self.update)
            self.element = Label(root, textvariable=self._value)


        #* Add the tooltip
        if self.tooltip is not None:
            self.tooltipObj = Tooltip(self.element, self.tooltip)

        #* Add the update function, if there is one.
        if self.type not in FUNC_TYPES and self.type != 'color':
            def _update(*_):
                self.update()
                self.updateFunc(self.value, *self.params, **self.kwparams)

            self._value.trace_add('write', _update)

        #* Return the elements to options menu so it can take care of packing them
        return (title, (label, self.element))

    def colorPicker(self):
        self._value = colorchooser.askcolor(title="Choose Color")[0]
        if self._value is not None:
            self.buttonColor.configure(f'{self.saveName}.TButton', background=rgbToHex(self._value), focuscolor='maroon')#rgbToHex(darken(self.value, 20)))
            # self.buttonColor.configure(rgbToHex(self._value)

    def call(self, params=None, kwparams={}):
        if self.type in FUNC_TYPES:
            if params is None:
                params = self.params
            if kwparams is None:
                kwparams = self.kwparams

            self.returnVal = self.func(*params, *kwparams)
            return self.returnVal
        else:
            raise AttributeError("Cannot call a non-function option")

    def update(self):
        if self.type == 'color':
            if self._value is not None:
                self.value = self._value
        elif self.type in FUNC_TYPES:
            self.value = self._value
        elif self.type in (tuple, list, set):
            self.value = self.element.get()
        else:
            self.value = self._value.get()

        self.save()

    def get(self):
        if self.enum is not None:
            return getattr(self.enum, self.value)
        # elif self.type is StringVar:
        #     return self.
        else:
            return self.value

    def set(self, val):
        if isinstance(val, Enum):
            self.value = val.name
        else:
            self.value = val

            if self.type is StringVar:
                self._value.set(val)

    def __invert__(self):
        if self.enum is not None:
            return getattr(self.enum, self.value)
        else:
            return self.value

    def truth(self):
        if self.enum is not None:
            return getattr(self.enum, self.value)
        else:
            return self.value

    def save(self):
        with open(SETTINGS_FILE, "r") as jsonFile:
            data = json.load(jsonFile)

        data[self.saveName] = self.value

        with open(SETTINGS_FILE, "w") as jsonFile:
            json.dump(data, jsonFile)

    def __lt__(self, option):
        myIndex    = self.order.index(self.type)
        theirIndex = self.order.index(option.type)
        if myIndex == theirIndex:
            if self.label == option.label:
                if self.title == option.title:
                    return self.widgetText < option.widgetText
                else:
                    return self.title < option.title
            else:
                return self.label < option.label
        else:
            return myIndex < theirIndex

    def __gt__(self, option):
        myIndex    = self.order.index(self.type)
        theirIndex = self.order.index(option.type)
        if myIndex == theirIndex:
            if self.label == option.label:
                if self.title == option.title:
                    return self.widgetText > option.widgetText
                else:
                    return self.title > option.title
            else:
                return self.label > option.label
        else:
            return myIndex > theirIndex

    def __str__(self):
        return f'Opt[{self.type}: {self.value}, {self._value}]'



class OptionsMenu(ScrolledFrame):
    def __init__(self, win, *options, styleOptionTab='General'):
        super().__init__(win, backgroundColor=(49, 54, 59))
        self.win = win
        self.win.title = 'Options'

        s = generateStyle()

        #* Add the style Option
        if styleOptionTab is not None and len(styleOptionTab):
            style = Option(s.theme_names(), 'GUI Theme', tab=styleOptionTab, currentItem='default', updateFunc=s.theme_use, tooltip='The theme to use for this options menu', var='style')
            s.theme_use(style.get())
            options += (style,)

        #* Put it in the correct place on screen
        screenXpos = int((self.winfo_screenwidth()  / 2) - 250) # (int(winSize[0]) / 2))
        screenYpos = int((self.winfo_screenheight() / 2) - 150) # (int(winSize[1]) / 2))
        self.win.wm_geometry(f'+{screenXpos}+{screenYpos}')

        self.options = options
        #* A sorted list of unique tabnames
        self.tabNames = sorted(list(set([i.tab for i in options])))
        # Make sure the General tab is first
        if 'General' in self.tabNames:
            self.tabNames.remove('General')
            self.tabNames.insert(0, 'General')
        self.tabs = {}



        #* track changes to the canvas and frame width and sync them,
        #   also updating the scrollbar
        # def _configure_interior(event):
        #     #* update the scrollbars to match the size of the inner frame
        #     size = (scrolledFrame.winfo_reqwidth(), scrolledFrame.winfo_reqheight())
        #     self.canvas.config(scrollregion="0 0 %s %s" % size)
        #     if scrolledFrame.winfo_reqwidth() != self.canvas.winfo_width():
        #         #* update the canvas's width to fit the inner frame
        #         self.canvas.config(width=scrolledFrame.winfo_reqwidth())
        # scrolledFrame.bind('<Configure>', _configure_interior)

        # def _configure_canvas(event):
        #     if frame.winfo_reqwidth() != self.notebook.winfo_width():
        #         #* update the inner frame's width to fill the canvas
        #         self.notebook.itemconfigure(interior_id, width=self.canvas.winfo_width())
        # self.canvas.bind('<Configure>', _configure_canvas)



        self.grid()
        self.createUI()

    def createUI(self):
        def scrollUp(event):
            self.canvas.yview_scroll(-SCROLL_SPEED, 'units')

        def scrollDown(event):
            self.canvas.yview_scroll(SCROLL_SPEED, 'units')

        #* Create a notebook in the scrolled frame
        self.notebook = Notebook(self.scrolledFrame)

        #* Create all the important widgets in the notebook frames
        for i in self.tabNames:
            self.tabs[i] = Frame(self.notebook)
            # HEIGHT_OF_BUTTONS = 100
            # if self.tabs[i].grid_bbox()[3] < self.winfo_height() - HEIGHT_OF_BUTTONS:
                # self.tabs[i].grid_propagate(self.winfo_height() - HEIGHT_OF_BUTTONS)



        currCol = 0

        #* Go through and create the elements
        for i in self.options:
            for tmp in (i.create(self.tabs[i.tab]),):
                title, le = tmp
                label, element = le
                currCol += 1
                if title   is not None: title.grid(row=currCol - 1)
                if label   is not None: label.grid(column=0, row=currCol, sticky='w')
                if element is not None: element.grid(column=1, row=currCol, sticky='w')
                currCol += 1

        #* Add tab names to the tabs
        for name, tab in self.tabs.items():
            self.notebook.add(tab, text=name)

        def adjustSize(event):
            # self.notebook.configure()
            pass

        self.win.bind('<Escape>', self.exit)
        self.win.bind('o', self.exit)
        self.win.bind('<Return>', self.save)
        self.win.bind('<Button-4>', scrollUp)
        self.win.bind('<Button-5>', scrollDown)
        self.win.bind('<Tab>', self.switchTabForward)
        self.win.bind('<Shift-KeyPress-Tab>', self.switchTabBackward)
        self.win.bind('<Shift-ISO_Left_Tab>', self.switchTabBackward)
        # self.win.bind_all(func=print)
        self.win.bind('<Configure>', print)
        self.win.bind('<Configure>', adjustSize)

        self.notebook.grid(sticky='nsew') #fill='both', side='top'

        # Label( self, text='\n').pack()
        Button(self, text='Save', command=self.save).pack()
        Button(self, text="Cancel", command=self.win.destroy).pack()
        Button(self, text='Restore to Defaults', command=self.restore).pack()

    def switchTabForward(self, event):
        try:
            self.notebook.select(self.notebook.index(self.notebook.select()) + 1)
        except TclError:
            self.notebook.select(0)

    def switchTabBackward(self, event):
        tmp=self.notebook.index(self.notebook.select())

        if tmp == 0:
            self.notebook.select(len(self.tabs) - 1)
        else:
            self.notebook.select(tmp - 1)

    def restore(self):
        for k in self.options:
            i.restoreDefault()

    def save(self, event=None):
        print('Saving settings...')
        for i in self.options:
            i.update()
        self.win.destroy()

    def exit(self, _):
        self.win.destroy()
