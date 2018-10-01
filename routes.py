from flask import Flask, url_for, request, render_template
import random
import string
from flask_npcgen import app
import npcgen.npcgen as genny

npc_generator = None


def random_string(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


@app.route('/')
def hello():
    return 'hello'


@app.route('/npc', methods=['GET', 'POST'])
def npc():
    global npc_generator
    if not npc_generator:
        npc_generator = genny.NPCGenerator()

    if request.method == 'POST':
        seed = request.form['seed']
        race_choice = request.form['race']
        class_choice = request.form['class']
        hd = int(request.form['hd'])

    if request.method == 'GET':
        seed = random_string(10)
        race_choice = random.choice(npc_generator.get_options('race'))[0]
        class_choice = random.choice(npc_generator.get_options('class'))[0]
        hd = random.randint(1, 20)

    npc = npc_generator.new_character(race_template_name=race_choice,
                                      class_template_name=class_choice,
                                      seed=seed,
                                      hit_dice_num=hd,)
    stat_block = npc.build_stat_block()
    plaintext=stat_block.display()
    stat_block_dict = stat_block.get_dict()

    html_traits = []
    for entry in stat_block_dict['passive_traits']:
        html_traits.append((entry[0], entry[1].replace("\n", "<br/>")))
    stat_block_dict['passive_traits'] = html_traits


    race_options = npc_generator.get_options('race')
    class_options = npc_generator.get_options('class')
    hd_range = list(range(1, 21))
    new_seed = random_string(10)
    # return render_template('statblock.html', stat_block=stat_block_dict)
    return render_template('npc.html', seed=new_seed, stat_block=stat_block_dict, race_options=race_options,
                           class_options=class_options, hd_range=hd_range, plaintext=plaintext)
