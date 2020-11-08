from pynput import keyboard, mouse

#* Keys
def on_press(key):
    try:
        print('{0} pressed'.format(key.char))
    except AttributeError:
        print('{0} pressed (Special Key)'.format(key))

def on_release(key):
    print('{0} released'.format(key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

def on_move(x, y):
    print('Pointer moved to {0}'.format(
        (x, y)))

#* Mouse
def on_click(x, y, button, pressed):
    print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released',
        (x, y)))
    if not pressed:
        # Stop listener
        return False

def on_scroll(x, y, dx, dy):
    print('Scrolled {0} at {1}'.format(
        'down' if dy < 0 else 'up',
        (x, y)))

# Collect events until released
# with mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
#     listener.join()

# ...or, in a non-blocking fashion:
mouseListener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)



# Collect events until released
# with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
#     listener.join()

# ...or, in a non-blocking fashion:
keyboardListener = keyboard.Listener(on_press=on_press, on_release=on_release)
keyboardListener.start()
mouseListener.start()

#