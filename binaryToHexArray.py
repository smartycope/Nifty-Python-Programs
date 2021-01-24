with open('/home/marvin/hello/C/MSP/Door_Alarm/seinfeld-theme_short.wav', 'rb') as f:
    with open('/home/marvin/hello/C/MSP/Door_Alarm/seinfeldTheme.h', 'w') as f2:
        for cnt, i in enumerate(f.read().hex()):
            if not cnt % 2:
                f2.write(', 0x')
            f2.write(i)