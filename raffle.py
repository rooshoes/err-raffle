import random
from errbot import BotPlugin, botcmd
from errbot.templating import tenv
from errbot.core_plugins.acls import glob
from time import sleep

import logging
log = logging.getLogger(__name__)

class Raffle(BotPlugin):
    """A plugin to pick a random user from the userlist"""
    min_err_version = '1.6.0'
    max_err_version = '2.1.0'

    def get_configuration_template(self):
        """Defines the configuration structure this plugin supports
        You should delete it if your plugin doesn't use any configuration like this"""
        return {'PREFIX': "WINNER:", 'IGNORED': ['*' + self.bot_config.CHATROOM_FN + '*'] + list(self.bot_config.BOT_ADMINS) }

    def configure(self, config):
        if config:
            if type(config) != dict:
                raise Exception('Wrong configuration type')

            if not 'PREFIX' in config:
                raise Exception('Wrong configuration type, it should contain PREFIX')

        super(Raffle, self).configure(config)

    @botcmd
    def spin(self, msg, args):
        if not glob(msg.frm, self.bot_config.BOT_ADMINS):
            return "You're not my dad!"

        try:
            room = msg.frm.room
        except AttributeError:
            room = self._bot.rooms()[0]

        viewers = [x for x in room.occupants if not glob(x.person, self.config['IGNORED'])]
        if not viewers:
            return "sorry, pool's empty."

        winner = random.choice(viewers).nick
        prefix_text = self.config['PREFIX']

        dest = room if msg.is_group else msg.frm
        self.send(dest, tenv().get_template('prefix.html').render( viewers=viewers ))
        if not (args == 'quick'):
            sleep(1)
            for i in range(5):
                self.send(dest, ' :catface: ' * i)
                sleep(1)
            sleep(2)
        self.send(dest, tenv().get_template('winner.html').render( prefix=prefix_text, winner=winner ))
