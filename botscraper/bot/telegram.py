''' Telegram Objects '''

import os
import datetime
from telegram import Update
from telegram.ext import (
        Updater,
        CommandHandler,
        MessageHandler,
        Filters,
        CallbackContext,
        PicklePersistence,
)
from ..core import scraper


class TBot(scraper.ETL):

    def __init__(self):
        super().__init__()
        self.load_bot_cfg()

    def load_bot_cfg(self) -> None:
        self.token = os.environ[self.cfg['TELEGRAM']['token']]
        self.config.alarm = self.cfg['TELEGRAM']['ETL_SCHEDULE'].split(',')
        persistence = PicklePersistence(filename='output/conversationbot.pickle',
                                        store_callback_data=True)
        self.updater = Updater(self.token, persistence=persistence,
                               arbitrary_callback_data=True)

    def load_cfg(self) -> None:
        pass

    def notify(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.message.chat_id
        clock = datetime.time(int(self.config.alarm[0]) + 3, # convert UTC
                              int(self.config.alarm[1]),
                              int(self.config.alarm[2]),
                              int(self.config.alarm[3]))
        job_removed = self.remove_job_if_exists(str(chat_id), context)

        context.job_queue.run_daily(self.check_news,
                                    clock, days=tuple(range(7)),
                                    context=chat_id, name=str(chat_id))
        text = 'Notification was enabled!'
        if job_removed:
            text += ' Old one was removed.'

        update.message.reply_text("\U0001F916 " + text)

    def non_notify(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.message.chat_id
        job_removed = self.remove_job_if_exists(str(chat_id), context)
        text = '\U0001F916 Notification was disabled!'
        if job_removed:
            text += ' Old one was removed!'
        update.message.reply_text(text)

    @staticmethod
    def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
        current_jobs = context.job_queue.get_jobs_by_name(name)
        if not current_jobs:
            return False
        for job in current_jobs:
            job.schedule_removal()
        return True

    def check_news(self, context: CallbackContext) -> None:
        job = context.job
        self.run()
        context.bot.send_message(job.context, text='\U0001F31E Hi, Good Morning!!!')
        if len(self.c_news) <= 1:
            context.bot.send_message(job.context, text='There is: ' + str(len(self.c_news)) + ' contest today!')
        else:
            context.bot.send_message(job.context,
                                     text='There are: ' + str(len(self.c_news)) +
                                     ' contest today!')

        s_df = self.df[self.df['URL'].isin(self.c_news)]
        for cnt in s_df.iterrows():
            contest = dict(cnt[1])
            context.bot.send_message(job.context,
                                     text='\U0001F6A8 [' + contest['Role'] + ']'
                                     '(' + contest['URL'] + ') \U0001F6A8\n'
                                     '*State*: ' + contest['State'] + '\n'
                                     '*Until*: '+ contest['Until'].strftime("%d/%m/%Y") + '\n'
                                     '*Keywords*: '+ contest['Keys'], parse_mode='Markdown')

    @staticmethod
    def help(update: Update, _) -> None:
        update.message.reply_text(
            '\U0001F916 * Command List* \U0001F916\n'
            '\U0001F4DA */help* to see all commands\n'
            '\U0001F6A7 */set* <keyword> to add new keyword\n'
            '\U0001F6A7 */unset* <keyword> to remove keyword\n'
            '\U0001F514 */notify* to enable Notification!\n'
            '\U0001F515 */non_notify* to disable Notification!\n'
            '\U0001F4DD */keywords* to show all keywords!\n'
            '\U0001F4DD */show* <keyword>  to list contest by keyword!\n'
            '\U0001F4D1 */show* to show all filtered contests!\n',
            parse_mode='Markdown')

    def get_keywords(self, update: Update, _) -> None:
        keys = ', '.join(map(str, self.config.keywords))
        update.message.reply_text('\U0001F916 *The keywords are:* \n*' + keys + '*',
                                  parse_mode='Markdown')

    def show_contest(self, update: Update, context: CallbackContext) -> None:
        key = ' '.join(context.args)
        if key:
            s_df = self.last_df[self.last_df['TxtBody'].str.contains(key)]
            update.message.reply_text('Searching by ' + key)
        else:
            s_df = self.last_df[s_df.Keys != '']
            update.message.reply_text('Searching all')
        for cnt in s_df.iterrows():
            contest = dict(cnt[1])
            try:
                str_date = datetime.datetime.strptime(contest['Until'], '%Y-%m-%d %H:%M:%S')
                str_date = str_date.strftime("%d/%m/%Y")
            except ValueError:
                str_date = self.try_date('')
            update.message.reply_text('[' + contest['Role'] + ']' + '(' + contest['URL'] + ')\n' +
                                      '*State*: ' + contest['State'] + '\n' +
                                      '*Until*: ' + str_date + '\n' +
                                      '*Keywords*: ' + (key if key else contest['Keys']), parse_mode='Markdown')

    def add_key(self, update: Update, context: CallbackContext) -> None:
        new_key = ' '.join(context.args)
        if new_key and not new_key in self.config.keywords:
            self.cfg['GERAL']['keywords'] += ',' + new_key
            with open('config/configs.cfg', 'w') as configfile:
                self.cfg.write(configfile)
            # reload
            self.load_cfg()
            update.message.reply_text(new_key + " was add!")
        elif new_key in self.config.keywords:
            update.message.reply_text(
                '\U0001F916 The keyword: *' + new_key + '* already exists', parse_mode='Markdown')
        else:
            update.message.reply_text("\U0001F916 Please, type /set <keyword>")

    def remove_key(self, update: Update, context: CallbackContext) -> None:
        new_key = ' '.join(context.args)
        if new_key and new_key in self.config.keywords:
            self.config.keywords.remove(new_key)
            self.cfg['GERAL']['keywords'] = ','.join(self.config.keywords)
            with open('config/configs.cfg', 'w') as configfile:
                self.cfg.write(configfile)
            # reload
            self.load_cfg()
            update.message.reply_text('\U0001F916 ' + new_key + ' was removed!')
        elif not new_key in self.config.keywords:
            update.message.reply_text(
                '\U0001F916 The keyword: *' + new_key + '* not exists', parse_mode='Markdown')
        else:
            update.message.reply_text('\U0001F916 Please, type /unset <keyword>')

    def start_etl(self, update: Update, _) -> None:
        update.message.reply_text('\U0001F916 Updating ...')
        self.run()
        update.message.reply_text('\U0001F916 Finished!')

    def go_idle(self) -> None:
        dispatcher = self.updater.dispatcher
        dispatcher.add_handler(CommandHandler("notify", self.notify))
        dispatcher.add_handler(CommandHandler("non_notify", self.non_notify))
        dispatcher.add_handler(CommandHandler("help", self.help))
        dispatcher.add_handler(CommandHandler("start", self.help))
        dispatcher.add_handler(CommandHandler("keywords", self.get_keywords))
        dispatcher.add_handler(CommandHandler("set", self.add_key))
        dispatcher.add_handler(CommandHandler("unset", self.remove_key))
        dispatcher.add_handler(CommandHandler("update", self.start_etl))
        dispatcher.add_handler(CommandHandler("show", self.show_contest))
        dispatcher.add_handler(MessageHandler(
            Filters.text & ~Filters.command, self.help))

        self.updater.start_polling()
        self.updater.idle()
