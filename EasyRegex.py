import re


class EasyRegex:
    """ EasyRegex! A Class for making regular expressions syntax easier.

        Note: This class does NOT actually do any regular expression processing.
              That's for the re module to do. All this class does is generate a
              regex command which is available on calling str() (the method or
              the cast), or compile(), which compiles it into the re module for
              you.

        Usage:
            EasyRegex().match("Foo{").ifProceededBy(EasyRegex().word().match("}")))
            ->
            "Foo\{(?=\w+\})"

            To start any regex command, call the default constructor, or if you
            already know some regex syntax, call the constructor with a base command.
            Then just chain method calls in the order you wish to construct the command,
            ending with .str(), .compile(), or nothing (it automatically casts to a
            string).
            Global flags such as caseInsensitive() and matchMultiLine() are available,
            and can be used at any point in the chain. However, they do not work with the
            python re module, so don't use them.
            Assertions ifProceededBy(), ifPreceededBy(), and their inverts are available.
            Note that any method that takes a statement can take a brand new chain as a
            parameter.
            You do still have to escape the \ character (i.e. \\), however all other
            characters you do not have to escape, that's automatically handled for you.
    """

    def __init__(self, expr=''):
        self.regexpr = expr
        self.globalFlags = ""
        self.passive = False

    def __str__(self):
        # return '(' + ('?:' if self.passive else '') + self.regexpr + self.globalFlags + ')'
        return self.regexpr + self.globalFlags

    def __repr__(self):
        return 'RegexGroup("' + str(self) + '")'

    def __add__(self, thing):
        return thing + str(self)

    def __iadd__(self, thing):
        thing += str(self)


    def compile(self):
        return re.compile(str(self))

    def str(self):
        return str(self)

    def correctInput(self, i):
        i = str(i)
        # i = re.sub(r'\\', r'\\', i)
        # i = re.sub(r'\((?<!\\)', r'\(', i)
        i = re.sub(r'(?<!\\)\)', r'\)', i)
        i = re.sub(r'(?<!\\)\[', r'\[', i)
        i = re.sub(r'(?<!\\)\]', r'\]', i)
        i = re.sub(r'(?<!\\)\{', r'\{', i)
        i = re.sub(r'(?<!\\)\}', r'\}', i)
        return i

    def wordStartsWith(self, group):
        group = self.correctInput(group)
        self.regexpr = group + r'\<' + self.regexpr
        return self

    def wordEndsWith(self, group):
        group = self.correctInput(group)
        self.regexpr += r'\>' + group
        return self

    def startsWith(self, group):
        group = self.correctInput(group)
        self.regexpr = group + r'\A' + self.regexpr
        return self

    def endsWith(self, group):
        group = self.correctInput(group)
        self.regexpr += r'\Z' + group
        return self

    def match(self, group):
        group = self.correctInput(group)
        self.regexpr += group
        return self

    def isExactly(self, group):
        group = self.correctInput(group)
        self.regexpr += "^" + group + '$'

    def optional(self):
        self.regexpr += r'?'
        return self

    def multiOptional(self):
        self.regexpr += r'*'
        return self

    def matchMax(self):
        self.regexpr += r'+'
        return self

    def matchNum(self, num):
        self.regexpr += '{' + num + '}'
        return self

    def matchRange(self, min, max):
        self.regexpr += '{' + min + ',' + max + '}'
        return self

    def matchMoreThan(self, min):
        self.regexpr += '{' + (min - 1) + ',}'
        return self

    def whitespace(self):
        self.regexpr += r'\s'
        return self

    def whitechunk(self):
        self.regexpr += r'\s+'
        return self

    def digit(self):
        self.regexpr += r'\d'
        return self

    def number(self):
        self.regexpr += r'\d+'
        return self

    def word(self):
        self.regexpr += r'\w+'
        return self

    def wordChar(self):
        self.regexpr += r'\w'
        return self

    def notWhitespace(self):
        self.regexpr += r'\S'
        return self

    def notDigit(self):
        self.regexpr += r'\D'
        return self

    def notWord(self):
        self.regexpr += r'\W'
        return self

    def hexDigit(self):
        self.regexpr += r'\x'
        return self

    def octDigit(self):
        self.regexpr += r'\O'
        return self

    def anything(self):
        self.regexpr += r'.'
        return self

    def either(self, group, or_group):
        group = self.correctInput(group)
        or_group = self.correctInput(or_group)
        self.regexpr += rf'({group}|{or_group})'
        return self

    def anyOf(self, *groups):
        self.regexpr += r'['
        for i in groups:
            i = self.correctInput(i)
            self.regexpr += i
        self.regexpr += r']'
        return self

    def anyExcept(self, *groups):
        self.regexpr += r'[^'
        for i in groups:
            i = self.correctInput(i)
            self.regexpr += i
        self.regexpr += r']'
        return self

    def anyBetween(self, group, and_group):
        group = self.correctInput(group)
        and_group = self.correctInput(and_group)
        self.regexpr += r'[' + group + '-' + and_group + r']'
        return self

    def anyUppercase(self):
        self.regexpr += r' [A-Z]'
        return self

    def anyLowercase(self):
        self.regexpr += r' [a-z]'
        return self

    def anyLetter(self):
        self.regexpr += r'[A-Za-z]'
        return self

    def anyAlphaNum(self):
        self.regexpr += r'[A-Za-z0-9]'
        return self

    def anyDigit(self):
        self.regexpr += r'[0-9]'
        return self

    def anyHexDigit(self):
        self.regexpr += r'[0-9a-f]'
        return self

    def anyOctDigit(self):
        self.regexpr += r'[0-7]'
        return self

    def anyPunctuation(self):
        self.regexpr += r'[:punct:]'
        return self

    def spaceOrTab(self):
        self.regexpr += r'[ \t]'
        return self

    def anyBlank(self):
        self.regexpr += r'[ \t\r\n\v\f]'
        return self

    def anyControllers(self):
        self.regexpr += r'[\x00-\x1F\x7F]'
        return self

    def anyPrinted(self):
        self.regexpr += r'[\x21-\x7E]'
        return self

    def anyPrintedAndSpace(self):
        self.regexpr += r'[\x20-\x7E]'
        return self

    def anyAlphaNum_(self):
        self.regexpr += r'[A-Za-z0-9_]'
        return self

    def newLine(self):
        self.regexpr += r'\n'
        return self

    def carriageReturn(self):
        self.regexpr += r'\r'
        return self

    def tab(self):
        self.regexpr += r'\t'
        return self

    def verticalTab(self):
        self.regexpr += r'\v'
        return self

    def formFeed(self):
        self.regexpr += r'\f'
        return self

    def octalNum(self, num):
        self.regexpr += '\\' + num
        return self

    def hexNum(self, num):
        self.regexpr += r'\x' + num
        return self

    def matchGlobally(self):
        self.globalFlags += r'//g'
        return self

    def caseSensitive(self):
        return self

    def caseInsensitive(self):
        self.globalFlags += r'//i'
        return self

    # def caseInsensitive(self):
        # self.globalFlags += r'//i'
        # self.regexpr = re.sub(r'[A-Za-z]', , self.regexpr)
        # return self

    def matchMultiLine(self):
        self.globalFlags += r'//m'
        return self

    def treatAsSingleLine(self):
        self.globalFlags += r'//s'
        return self

    def greedy(self):
        return self

    def notGreedy(self):
        self.globalFlags += r'//U'
        return self

    def add(self, group):
        group = self.correctInput(group)
        self.regexpr += group
        return self

    def ifAtBeginning(self):
        self.regexpr = r'^' + self.regexpr
        return self

    def ifAtEnd(self):
        self.regexpr += r'$'
        return self

    def ifProceededBy(self, condition_group):
        condition_group = self.correctInput(condition_group)
        self.regexpr = self.regexpr + fr'(?={condition_group})'
        return self

    def ifNotProceededBy(self, condition_group):
        condition_group = self.correctInput(condition_group)
        self.regexpr = self.regexpr + fr'(?!{condition_group})'
        return self

    def ifPrecededBy(self, condition_group):
        condition_group = self.correctInput(condition_group)
        self.regexpr += fr'(?<={condition_group})'
        return self

    def ifNotPrecededBy(self, condition_group):
        condition_group = self.correctInput(condition_group)
        self.regexpr += fr'(?<!{condition_group})'
        return self
