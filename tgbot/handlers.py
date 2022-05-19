

import random
from django.db.models.fields import BLANK_CHOICE_DASH
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update
from telegram import ParseMode
from tgbot.utils import get_quadratic_func_plot, send_rand_parabola_and_save_answer

from user import models# Answer, User


def start(update: Update, context: CallbackContext):
    models.User.objects.get_or_create(tg_id=update.effective_chat.id)
    update.message.reply_text('Привет! С моей помощью ты научишься понимать знаки коэффециентов параболы. Я тебе буду отправлять параболу, а ты мне - ответ. Например, вот парабола:')
    update.message.reply_photo(get_quadratic_func_plot(1,-2,3, set = {'title':r'$x^{2}-2x+3$'}))
    update.message.reply_text('В этом случае я ожидаю от тебя такой ответ:')
    update.message.reply_text('<b>+-+</b>', parse_mode=ParseMode.HTML)
    update.message.reply_text('Если захочешь пропустить вопрос, отправь /skip')
    update.message.reply_text('Давай начнём:')
    send_rand_parabola_and_save_answer(update, context)

def enter_answer(update: Update, context: CallbackContext):
    blank_answer: models.Answer = models.Answer.objects.get(user__tg_id = update.effective_chat.id, answer=None)
    blank_answer.answer = update.message.text
    blank_answer.save()
    print(repr(blank_answer.right_answer))
    if blank_answer.right_answer == update.message.text:
        update.message.reply_text('Поздравляю, правильно!')
        update.message.reply_text(random.choice('🥳🎇🎆🎉'))
        send_rand_parabola_and_save_answer(update, context)
    else:
        update.message.reply_text('Неверно! Попробуй еще раз или нажми /skip')
        blank_answer.pk=None
        blank_answer.answer=None
        blank_answer.save()

def skip(update: Update, context: CallbackContext):
    send_rand_parabola_and_save_answer(update, context)
    





