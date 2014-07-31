import string
import csv
import cmd
import sys

#global variables
questions = None
words = {}
phrases = {}


def extract_data(filename, mode='rb', delimiter=',', quotechar='"',
                 skipcols=1, minlength=3):
    """
    Extracts text from a csv file in order to discover how many times each
    word appears. Then  arranges this data in 2 dictionaries, one for the
    words, sorted by occurrences, and another one containing the phrases
    associated with these words.
    """
    global questions, words, phrases

    with open(filename, 'rb') as f:
        data = csv.reader(f, delimiter=delimiter, quotechar=quotechar)
        for row in data:
            if not questions:
                questions = row

            #go through the cols of a row
            for col in row[skipcols:]:
                exclude = set(string.punctuation)
                s = ''.join(ch if ch not in exclude else ' ' for ch in col)
                for word in s.split():
                    if len(word) < minlength:
                        continue

                    if word not in words:
                        words.update({word: 1})
                        phrases.update({word: []})
                    else:
                        words[word] += 1
                        phrases[word].append(col)

        words = sorted(words.items(), key=lambda item: item[1], reverse=True)
        return questions, words, phrases


class CLI(cmd.Cmd):
    """
    A simple command line tool based on cmd module
    (https://docs.python.org/2/library/cmd.html)

    Avaliable commands:
    - top {n}: Prints the top {{n}} words
    - min {n}: Prints the words that repeats at least {n} times
    - exp {word}: Explore the phrases that the {word} appears in
    - quit/q: Exit
    """
    global questions, words, phrases

    def __init__(self):
        cmd.Cmd.__init__(self)
        print 'The file was processed successfully!'
        self.prompt = 'Please type a command > '

    def _print_words(self, data):
        for w, n in data:
            print "'%s' (%d)" % (w, n)

    def do_top(self, arg):
        top = 0
        if arg:
            try:
                top = int(arg)
            except ValueError:
                print "*** argument should be number of words you want to see"

        print "-----TOP %s WORDS-----" % (top, )
        if top:
            self._print_words(words[:top])
        else:
            self._print_words(words)

    def do_min(self, arg):
        try:
            _min = int(arg)
        except ValueError:
            print "*** argument should be number of words you want to see"

        data = [(x, n) for x, n in words if n >= _min]
        print "-----MIN %d OCCURRENCES-----" % (_min, )
        self._print_words(data)

    def do_exp(self, arg):
        print '-----EXPLORING THE WORD %s-----' % (arg, )
        for p in phrases.get(arg):
            print '%s \n----------------\n' % (p.replace('\\n', ''))

    def do_quit(self, arg):
        sys.exit(1)

    def help_top(self):
        print "syntax: top {n}"
        print "-- Prints the top {{n}} words"

    def help_min(self):
        print "syntax: top {n}"
        print "-- Prints the words that repeats at least {n} times"

    def help_exp(self):
        print "syntax: top {word}"
        print "-- exp {word}: Explore the phrases that the {word} appears in"

    def help_quit(self):
        print "syntax: quit",
        print "-- terminates the application"

    def help_q(self):
        return self.help_quit()

    # shortcuts
    do_q = do_quit

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("ERROR: Please tell where is the file to be analyzed\n"
                 "ex: python analyzer.py /path/to/mydata.csv")

    argv = sys.argv
    try:
        extract_data(argv[1])
    except IOError:
        print "*** Could not open the %s file" % (argv[1])

    cli = CLI()
    cli.cmdloop()
