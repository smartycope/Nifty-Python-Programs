#!/usr/bin/python

# For adding colors to the description
from CommonUsefulFunctions import TerminalColors
import requests, re, os, sys, argparse

# For getting the image and the description
from urllib.request import urlopen
from urllib.parse import urlparse, urljoin
from urllib.error import URLError
from bs4 import BeautifulSoup as bs

# For the progress bar
from tqdm import tqdm

# For displaying the image
try:
    import tkinter as tk
    from PIL import ImageTk, Image
    from io import BytesIO
except ImportError:
    DO_IMAGE = False


savePath    = '/home/marvin/Media/Pictures/Space Pictures'
url         = "https://apod.nasa.gov/apod/astropix.html"
description = 'A command line program for the Astronomy Picture of the Day'

parser = argparse.ArgumentParser(description=description)
parser.add_argument('command',                      help='What to do (save, description, save-description, display/show)',    nargs='?')
parser.add_argument('-s', '--save',                 help='Save the image',                                      type=str, nargs='?', default='')
parser.add_argument('-d', '--description',          help='Print the desciption',                                type=str, nargs='?', default='')
parser.add_argument('-S', '--no-save-description',  help='Save the description as a text file with the images', action='store_true')
parser.add_argument('-C', '--no-colors',            help='Don\'t display colors',                               action='store_true')
parser.add_argument('-P', '--no-progress-bar',      help='Don\'t show the progres bar when saving',             action='store_true')
parser.add_argument('-D', '--display', '--show',    help='Display the image',                                   action='store_true', dest='show')
args = parser.parse_args()

#* Makes it that much faster
try:
    if not (args.show and os.path.isfile(os.path.join(savePath, getTitle() + '.jpeg'))):
        soup = bs(urlopen(url).read(), 'lxml')
except urllib.error.URLError:
    print('No internet connection')
    exit(0)

def getTitle():
    return soup.b.string.strip()

IMAGE_NAME       = os.path.join(savePath, getTitle()) if (args.save        is None or args.save == '')        else args.save
DESCRIPTION_NAME = os.path.join(savePath, getTitle()) if (args.description is None or args.description == '') else args.description

if len(sys.argv) == 1 or (len(sys.argv) == 2 and args.no_colors):
    args.command = 'description'

if args.command == None:
    args.command = ''


def getDescription():
    des = str()
    fudge = True

    for string in soup.body.contents[5].stripped_strings:
        if not fudge:
            des += string
            des += ' '
        fudge = False

    des = re.sub(r'\s', r' ', des)
    des = re.sub(r'[ ][.]', r'.', des)
    des = re.sub(r'[ ][,]', r',', des)
    des = re.sub(r'[ ][ ]', r' ', des)
    return des


def addLines(string, width):
    pos = findSpace = 0

    while pos < len(string) - width:
        pos += width - 1
        findSpace = pos

        while string[findSpace - 1] != ' ':
            findSpace -= 1

        string = string[:findSpace] + '\n' + string[findSpace:]

    return string


def center(string):
    for _ in range(int((os.get_terminal_size().columns - len(string)) / 2)): string = ' ' + string
    return string

def isValid(url):
    """ Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def getAllImages(url, verbose):
    """Returns all image URLs on a single `url`
    """
    soup = bs(requests.get(url).content, "html.parser")

    urls = []
    for img in tqdm(soup.find_all("img"), "Fetching Image") if verbose else soup.find_all("img"):
        img_url = img.attrs.get("src")
        if not img_url:
            # If img does not contain src attribute, just skip
            continue

        # Make the URL absolute by joining domain with the URL that is just extracted
        img_url = urljoin(url, img_url)

        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass


        # If the url is valid
        if isValid(img_url):
            urls.append(img_url)
    return urls

def download(url, pathname, progressBar):
    """ Downloads a file given an URL and puts it in the folder 'pathname'
    """
    #* if path doesn't exist, make that path dir
    # if not os.path.isdir(pathname):
    #     os.makedirs(pathname)

    #* Download the body of response by chunk, not immediately
    response = requests.get(url, stream=True)

    #* Get the total file size
    file_size = int(response.headers.get("Content-Length", 0))

    if progressBar:
        #* Progress bar, changing the unit to bytes instead of iteration (default by tqdm)
        progress = tqdm(response.iter_content(1024), f"Downloading {getTitle()}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)

    with open(pathname, "wb") as f:
        for data in progress:
            #* Write data read to the file
            f.write(data)
            if progressBar:
                #* Update the progress bar manually
                progress.update(len(data))

def saveImage(url, filepath, progressBar):
    #* Get all images and download the first one (there should only be 1)
    try:
        download(getAllImages(url, progressBar)[0], filepath + '.jpeg', progressBar)
    except:
        print('Today\'s APOD doesn\'t seem to be a picture. It\'s probably a video. Here\'s a link: https://apod.nasa.gov/apod/astropix.html')
        exit(0)

def saveDescription(filepath):
    with open(filepath + '.txt', 'w') as f:
        f.write(addLines(getDescription(), 80))

def displayImage(url, progressBar):
    #* This should work, but it doesnt.
    # img = Image.open(requests.get(getAllImages(url, progressBar)[0], stream=True).raw)
    # img.show()

    title = getTitle()
    file = os.path.join(savePath, title + '.jpeg')

    root = tk.Tk()
    root.title(title)

    print(file)

    if os.path.isfile(file):
        img = ImageTk.PhotoImage(Image.open(file))
    else:
        response = requests.get(getAllImages(url, progressBar)[0])
        img = ImageTk.PhotoImage(Image.open(BytesIO(response.content)))

    panel = tk.Label(root, image=img)
    panel.pack(side="bottom", fill="both", expand="yes")
    root.mainloop()


if __name__ == "__main__":
    if args.command.lower() in ['save', 's'] or args.save != '':
        saveImage(url, IMAGE_NAME, not args.no_progress_bar)

    if args.command in ['save-description', 'saveDescription', 'save description', 'sd'] or \
       (args.description is not None and args.description != '') or \
       (args.command.lower() == 'save' and not args.no_save_description):
        saveDescription(DESCRIPTION_NAME)
        print('Saved!')

    if args.command.lower() in ['description', 'd'] or args.description is None:
        if not args.no_colors: print(TerminalColors.CYAN)
        print(center(getTitle()))
        if not args.no_colors: print(TerminalColors.BLUE, end='')
        print(addLines(getDescription(), os.get_terminal_size().columns - 5))
        if not args.no_colors: print(TerminalColors.RESET)

    if args.command.lower() in ['show', 'display', 'sh'] or args.show:
        displayImage(url, not args.no_progress_bar)
        # displayImage(url, False)
