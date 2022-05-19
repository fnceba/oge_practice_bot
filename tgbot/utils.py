import matplotlib
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update

from user import models# Answer, User
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy
import io
import random

def arrowed_spines(fig, ax):

    xmin, xmax = ax.get_xlim() 
    ymin, ymax = ax.get_ylim()

    # removing the default axis on all sides:
    for side in ['bottom','right','top','left']:
        ax.spines[side].set_visible(False)

    # removing the axis ticks
    plt.xticks([]) # labels 
    plt.yticks([])
    ax.xaxis.set_ticks_position('none') # tick markers
    ax.yaxis.set_ticks_position('none')

    # get width and height of axes object to compute 
    # matching arrowhead length and width
    dps = fig.dpi_scale_trans.inverted()
    bbox = ax.get_window_extent().transformed(dps)
    width, height = bbox.width, bbox.height

    # manual arrowhead width and length
    hw = 1./40.*(ymax-ymin) 
    hl = 1./40.*(xmax-xmin)
    lw = 1. # axis line width
    ohg = 0.3 # arrow overhang

    # compute matching arrowhead length and width
    yhw = hw/(ymax-ymin)*(xmax-xmin)* height/width 
    yhl = hl/(xmax-xmin)*(ymax-ymin)* width/height

    # draw x and y axis
    ax.arrow(xmin, 0, xmax-xmin, 0., fc='k', ec='k', lw = lw, 
             head_width=hw, head_length=hl, overhang = ohg, 
             length_includes_head= True, clip_on = False) 
    ax.annotate('x',xy=(xmax-1/3, -1))

    ax.arrow(0, ymin, 0., ymax-ymin, fc='k', ec='k', lw = lw, 
             head_width=yhw, head_length=yhl, overhang = ohg, 
             length_includes_head= True, clip_on = False)
    ax.annotate('y',xy=(1/3, ymax-1/3))
    


def get_quadratic_func_plot(a,b,c, set = None):
    fig, ax = plt.subplots()
    x = numpy.linspace(-10, 10, 1000)
    y = a*x*x+b*x+c
    ax.grid(False)
    ax.axis([-10,10,-10,10])
    y_top = -b*b/(4*a) + c
    ax.set_ylim([min(-10,y_top-1), max(10, y_top+1)])
    arrowed_spines(fig,ax)
    if set:
        ax.set(**set)
    ax.plot(x,y)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf.read()

def send_rand_parabola_and_save_answer(update: Update, context: CallbackContext):
    blank_answer, _ = models.Answer.objects.get_or_create(user = models.User.objects.get(tg_id = update.effective_chat.id), answer=None)
    a=random.randint(-10,10) or 3
    b=random.randint(-10,10) or 3
    c=random.randint(-10,10) or 3
    blank_answer.right_answer = ''.join(map(lambda x: '+' if x>0 else '-',[a,b,c]))
    blank_answer.equasion = f'{a}x^2 + {b}x + {c}'
    blank_answer.save()
    update.message.reply_photo(get_quadratic_func_plot(a,b,c))
