
import random
from errbot import BotPlugin, botcmd


class Raffle(BotPlugin):
    """A simple plugin that returns random numbers"""
    min_err_version = '1.6.0'
    max_err_version = '2.1.0'

    @botcmd(split_args_with=None)
    def raffle(self, mess, args):
        """Get a random number between 1-100.
        Or Specify the range. [min]-[max] If only one arg is given its
        assumed to be max and min is set to 1"""
        try:
            if not args:
                a, b = 1, 100
            elif len(args) == 1:
                a, b = 1, int(args[0])
            elif len(args) == 2:
                a, b = int(args[0]), int(args[1])
            else:
                raise ValueError
        except ValueError:
            return "Sorry dude, i can only handle two arguments. Both must be numbers!"
        return u'{0} ({1}, {2})'.format(random.randint(a, b), a, b)
