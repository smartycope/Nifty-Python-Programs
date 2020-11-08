import clipboard, re, time

prevClip = ''
while True:
    clip = clipboard.paste()
    if prevClip != clip:
        prevClip = clip
        data = re.search(r'[-]?\d+ [-]?\d+ [-]?\d+', clip)
        if data is not None:
            data = clip[data.span()[0]:data.span()[1]]
            clipboard.copy(data)
    time.sleep(0.1)

    # /setblock -783 73 -5303 minecraft:spruce_planks
