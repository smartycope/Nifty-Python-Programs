import re


from random import randint
import math
from time import process_time

# Override the debug parameters and display the file/function for each debug call
#   (useful for finding debug calls you left laying around and forgot about)
debugCount = 0

DISPLAY_FILE = False
DISPLAY_FUNC = False

def debug(var=None, *more_vars, prefix: str='', name=None, merge: bool=False, repr: bool=False, calls: int=0,
          color: int=1, background: bool=False, itemLimit: int=10, showFunc: bool=False, showFile: bool=False,
          _isDebuggedCall: bool=False, _noRecall: bool=False) -> None: # pylint: disable=redefined-builtin
    """Print variable names and values for easy debugging.
    Call with no parameters to tell if its getting called at all, and call with a only a string to just display the string
    The format goes: Global_debug_counter[file->function()->line_number]: prefix data_type variable_name = variable_value
    Args:
        var: The variable or variables to print
        prefix: An additional string to print for each line
        merge: Put all the variables on the same line
        repr: Use __repr__() instead of __str__()
        calls: If you're passing in a return from a function, say calls=1
        color: 0-5. 5 different preset colors for easy distinction
        background: Use the background color instead of the forground color
        showFunc: Display what function you're calling from
        showFile: Display waht file you're calling from
    Usage:
        debug() -> prints 'HERE! HERE!' in bright red for you
        debug('I got to this point') -> prints that message for you
        debug(var) -> prints the type(var) var = {var}
        debug(func()) -> prints what the function returns
        debug(var, var1, var2) -> prints each var on their own line
        debug(var, name='variable') -> prints type(var) variable = {var}
        debug(var, var1, var2, name=('variable', 'variable2', 'variable3')) ->
            prints each var on their own line with the appropriate name
    """
    #* Make sure to always reset the color back to normal, in case we have an error inside this function
    try:
        from varname import nameof, VarnameRetrievingError
        from inspect import stack
        from os.path import basename
        from copy    import deepcopy

        global debugCount, DISPLAY_FUNC, DISPLAY_FILE
        debugCount += 1

        #* Get the function, file, and line number of the call
        s = stack()[(0 if _isDebuggedCall else 1) + calls]
        stackData = str(s.lineno)


        if itemLimit < 0:
            itemLimit = 1000000

        #* Colors
        # none, blue, green, orange, purple, cyan, alert red
        colors = ['0', '34', '32', '33', '35', '36', '31']

        if background:
            color += 10

        c = f'\033[{colors[color]}m'

        if var is None:
            if color == 1:
                print(f'\033[{colors[-1]}m', end='')
            else:
                print(c, end='')
        else:
            print(c, end='')

        #* Just print the "HERE! HERE!" message
        if var is None:
            print(f'{debugCount}[{stackData}]: HERE! HERE!')
            print('\033[0m', end='')
            return


        #* Shorten var if var is a list or a tuple
        # variables is a tuple of 2 item tuples that have the type as a string, and then the actual variable
        variables = ()
        for v in (var, *more_vars):
            if type(v) in (tuple, list, set) and len(v) > itemLimit:
                variables += ((type(v).__name__, str(v[0:round(itemLimit/2)])[:-1] + f', \033[0m...{c} ' + str(v[-round(itemLimit/2)-1:-1])[1:] + f'(len={len(v)})'),)
            elif type(v) in (tuple, list, set):
                variables += ((type(v).__name__, str(v) + f'(len={len(v)})'),)
            else:
                variables += ((type(v).__name__, v),)

        if DISPLAY_FUNC or showFunc:
            stackData = s.function + '()->' + stackData
        if DISPLAY_FILE or showFile:
            stackData = basename(s.filename) + '->' + stackData

        #* Actually get the names
        try:
            if name is None:
                try:
                    var_names = nameof(*[i[1] for i in variables], frame=2+calls, vars_only=False)
                except VarnameRetrievingError:
                    var_names = nameof(*[i[1] for i in variables], frame=2+calls)
            else:
                # This should work for tuples too
                if type(name) is list:
                    name = tuple(name)
                var_names = name

        #* If only a string literal is passed in, display it
        except VarnameRetrievingError as err:
            if type(var) is str:
                print(f"{debugCount}[{stackData}]: {prefix} {var}")
                print('\033[0m', end='')
                return
            else:
                raise err

        #* If it's not already a tuple, turn it into one
        if not isinstance(var_names, tuple):
            var_names = (var_names, )

        name_and_values = [f"{var_name} = {variables[i][1]!r}" if repr
                      else f"{var_name} = {variables[i][1]}"
                       for i, var_name in enumerate(var_names)]

        if merge:
            print(f"{debugCount}[{stackData}]: {prefix}{', '.join(name_and_values)}")
        else:
            for cnt, name_and_value in enumerate(name_and_values):
                print(f"{debugCount}[{stackData}]: {prefix}{variables[cnt][0].title()} {name_and_value}")
                # debugCount += 1

        print('\033[0m', end='')
    #* Catch the error and try again with an additional call
    except VarnameRetrievingError as err:
        if not _noRecall:
            debug(var, more_vars, prefix=prefix, name=name, repr=repr, merge=merge, calls=calls+2, color=color, background=background,
                    itemLimit=itemLimit, showFunc=showFunc, showFile=showFile, _isDebuggedCall=False, _noRecall=True)
        else:
            raise err


    finally:
        print('\033[0m', end='')


def debugged(var, prefix: str='', name=None, repr: bool=False, calls: int=0,
          color: int=1, background: bool=False, itemLimit: int=10, showFunc: bool=False, showFile: bool=False):
    """ An inline version of debug
    """

    debug(var, prefix=prefix, name=name, repr=repr, calls=calls+1, color=color, background=background,
          itemLimit=itemLimit, showFunc=showFunc, showFile=showFile, _isDebuggedCall=True)

    return var



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



# diff = Time(input("Start time: ")) - Time(input("End time: "))
# print(f"{diff.hour} hours and {diff.min} minutes")

# debug(Time(10, 30))
# debug(Time(10, 30, False))
# debug(Time(10, 30, True))
# debug(Time(10, 30, method=Time.MILITARY))
# debug(Time(10, 30, method=Time.UNKNOWN))
# debug(Time(10, 30, False, method=Time.MILITARY))
# debug(Time(10, 30, False, method=Time.UNKNOWN))
# debug(Time("10:30"))
# debug(Time("10:30 pM"))
# debug(Time("10:30 pm"))
# debug(Time("10:30 AM"))
# debug(Time("10:30 am"))
# debug(Time("10:30 p.m."))
# debug(Time("10:30 p.M."))
# debug(Time("10:30 a.m."))
# debug(Time("10:30 a.M."))
# debug(Time("13:30 a.m."))
# debug(Time("13:30 A.M."))
# debug(Time(" 13:30a.m."))
# debug(Time(" 13:30A.M."))
# debug(Time(" 13:30AM"))
# debug(Time(" 13:30am"))
# debug(Time(" 13:30AM  "))
# debug(Time(" 13:30am  "))
# debug(Time(10, 30, True) > Time(11, 30, True))
# debug(Time(10, 30, True) < Time(11, 30, True))
# debug(Time(10, 30, True) > Time(12, 30, False))
# debug(Time(10, 30, True) < Time(12, 30, False))
# debug(Time(1, 30, True) > Time(12, 30, False))
# debug(Time(1, 30, True) < Time(12, 30, False))
# debug(Time(1, 30, True) > Time(1, 30, False))
# debug(Time(1, 30, True) < Time(1, 30, False))
# debug(Time(10, 30, True) - Time(11, 0, True))
# debug(Time(10, 30, True) - Time(11, 30, True))
# debug(Time(10, 30, True) - Time(11, 15, True))
# debug(Time(11, 30, True) - Time(10, 15, True))
# debug(Time(10, 15, True) - Time(11, 30, True))
# debug(Time(11, 15, True) - Time(10, 30, True))
# debug(Time(10, 30, True) - Time(12, 30, False))
# debug(Time(11, 0, True) - Time(1, 30, False))
# debug(Time(1, 0, False) - Time(11, 0, True))
# debug(Time(12, 0, False) - Time(12, 30, False))
# debug(Time(1, 0, True) - Time(12, 30, False))
# debug(Time(2, 0, False) - Time(1, 0, False))
# debug(Time(2, 0, True) - Time(1, 0, True))
# debug(Time(10, 30) + Time(12, 30))
# debug(Time(1, 30, method=Time.UNKNOWN) + Time(2, 30, False))
# debug(Time(10, 30, Time.UNKNOWN) + Time(12, 30))
# debug(Time(10, 30, Time.MILITARY) + Time(12, 30))

# debug(Time('8'))


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
    except Exception as err:
        print("Error:", err)
    print(f"Total: {total}, Overtime: {overtimeTotal}")
