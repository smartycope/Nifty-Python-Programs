import re

from random import randint
import math
from time import process_time


class Time:
    MILITARY = False
    STANDARD = True
    UNKNOWN  = None

    def __init__(self, hour, minutes=None, am=None, method=True):
        if minutes is None and type(hour) is str:
            self._initWithStr(hour)
        else:
            self.hour = hour
            self.min  = minutes
            self.am = am if method is Time.STANDARD else None
            self.type = method
            if method is Time.STANDARD and am is None:
                raise TypeError("am param not specified")

        self.minutes = self.min
        self.method = self.type

    def _initWithStr(self, s):
        s.strip()
        self.type = Time.STANDARD

        self.am = re.search(r'(am|pm)|(a\.m\.|p\.m\.)', s, re.IGNORECASE)
        s = re.sub(r'(?i)(am|pm)|(a\.m\.|p\.m\.)', '', s, re.IGNORECASE)
        s.strip()
        if self.am:
            self.type = Time.STANDARD
        if self.am is not None:
            self.am = not ('p' in self.am.string.lower())

        # assert(':' in s)
        if ':' in s:
            h, m = re.split(r':', s, 1)

            self.hour = int(re.search(r'\d+', h).string)
            self.min  = int(re.search(r'\d+', m).string)
        else:
            self.hour = int(re.search(r'\d+', s).string)
            self.min  = 0

        if self.hour > 12:
            self.type = Time.MILITARY

    def __str__(self):
        return f"{self.hour}:{self.min:0>2}" + ((" am" if self.am else " pm") if self.type is self.STANDARD else '')

    def __sub__(self, time):
            # if self.type is not time.type and not (self.periodKnown(False) or time.periodKnown(False)):
            #     raise TypeError("Can't subtract a 12 hour time from a 24 hour time and assume the am/pm")
            # if self < time:
            #     carry = 0
            #     if self.min - time.min < 0:
            #         carry = 1
            #     return Time(self.hour - time.hour - carry, self.min - time.min + (60 if carry else 0), None, Time.UNKNOWN)
            # else:
            #     carry = 0
            #     if self.min - time.min < 0:
            #         carry = 1
            #     return Time(self.hour - (time.hour + 12) - carry, self.min - time.min + (60 if carry else 0), None, Time.UNKNOWN)

        # else:
        carry = 0
        if time.min - self.min < 0:
            carry = 1
        ans = Time(time.getMilitary().hour - self.getMilitary().hour - carry, time.min - self.min + (60 if carry else 0), None, Time.UNKNOWN)
        if ans.hour < 0:
            ans.hour += 24
        return ans

    def __add__(self, time):
        if self.type is Time.STANDARD and time.type is Time.STANDARD:
            raise UserWarning("I'm lazy. Finish this.")
        else:
            carry = 0
            if self.min + time.min > 59:
                carry = 1
            return Time(self.hour + time.hour + carry,
                        self.min  + time.min  - (60 if carry else 0),
                        method=Time.MILITARY if self.type is Time.MILITARY and time.type is Time.MILITARY else Time.UNKNOWN)

    def __iadd__(self, time):
        if self.type is Time.STANDARD and time.type is Time.STANDARD:
            raise UserWarning("I'm lazy. Finish this.")
        else:
            carry = 0
            if self.min + time.min > 60:
                carry = 1
            self.hour += time.hour + carry
            self.min  += time.min  - (60 if carry else 0)
            self.type = Time.MILITARY if self.type is Time.MILITARY and time.type is Time.MILITARY else Time.UNKNOWN
            return self

    def __gr__(self, time):
        # if not self.periodKnown(False) or not time.periodKnown(False):
        #     if self.hour == time.hour:
        #         return self.min > time.min
        #     else:
        #         return self.hour < time.hour
        # else:
        self.periodKnown()
        time.periodKnown()
        if self.getMilitary().hour == time.getMilitary().hour:
            return self.min > time.min
        else:
            return self.getMilitary().hour > time.getMilitary().hour

        # if self.type is Time.MILITARY and time.type is Time.MILITARY:
        #     if self.hour == time.hour:
        #         return self.min < time.min
        #     else:
        #         return self.hour < time.hour
        # else:
        #     if self.am == time.am:
        #         if self.hour == time.hour:
        #             return self.min < time.min
        #         else:
        #             return self.hour < time.hour
        #     else:
        #         return self.am < time.am

    def __lt__(self, time):
        # if not self.periodKnown(False) or not time.periodKnown(False):
        #     if self.hour == time.hour:
        #         return self.min < time.min
        #     else:
        #         return self.hour > time.hour
        # else:
        self.periodKnown()
        time.periodKnown()
        if self.getMilitary().hour == time.getMilitary().hour:
            return self.min < time.min
        else:
            return self.getMilitary().hour < time.getMilitary().hour

        # if self.type is Time.MILITARY and time.type is Time.MILITARY:
        #     if self.hour == time.hour:
        #         return self.min < time.min
        #     else:
        #         return self.hour < time.hour
        # else:
        #     if self.am == time.am:
        #         if self.hour == time.hour:
        #             return self.min < time.min
        #         else:
        #             return self.hour < time.hour
        #     else:
        #         return self.am < time.am

    def getMilitary(self):
        if self.type == Time.MILITARY:
            return self
        else:
            if self.am:
                return Time(self.hour, self.min, method=Time.MILITARY)
            elif not self.am:
                return Time(self.hour + 12, self.min, method=Time.MILITARY)
            else: # self.am is None
                raise TypeError("Can't convert 12 hour time to 24 hour time without am/pm specified")

    def getStandard(self):
        if self.type is Time.STANDARD:
            return self
        else:
            if self.hour > 12:
                return Time(self.hour - 12, self.min, False, Time.STANDARD)
            else:
                return Time(self.hour, self.min, True, Time.STANDARD)

    def periodKnown(self, throwErr=True):
        if self.type is Time.STANDARD and self.am is None:
            if throwErr:
                raise TypeError("am/pm is not specified")
            return False
        else:
            return True


total = Time(0, 0, method=Time.UNKNOWN)
overtimeTotal = Time(0, 0, method=Time.UNKNOWN)
overtime = Time(10, 00, False)

def exit(*args):
    print(f"{total.hour} hours and {total.min} minutes")
    print(f"Overtime: {overtimeTotal.hour} hours and {overtimeTotal.min} minutes")
    quit(*args)

def qinput(*args, **kwargs):
    i = input(*args, **kwargs)
    if i.lower() in ('q', 'quit', 'done', 'finished', 'end', 'die', 'exit'):
        exit(0)
    return i

while True:
    # total += Time(qinput("Start time")) - Time(qinput("End time"))
    # start = Time(qinput("Start time: "))
    # end   = Time(qinput("End time: "))
    try:
        start, end = re.split('-', qinput("Enter times: "), 1)
        start, end = Time(start), Time(end)
        if end > overtime:
            total += start - overtime
            overtimeTotal += overtime - end
        else:
            # Total: 18:40, Overtime: 2:15
            total += start - end

        if start - end > Time(8, 00, False):
            # print('greater than 8 hours')
            over = Time(8, 00, False) - (start-end)
            overtimeTotal += over

    except Exception as err:
        print("Error:", err)
    print(f"Total: {total}, Overtime: {overtimeTotal}")
