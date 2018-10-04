from flask import Flask, url_for, request, render_template, redirect
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


@app.route('/npc', methods=['GET'])
def npc():
    global npc_generator
    if not npc_generator:
        npc_generator = genny.NPCGenerator()

    if request.method == 'GET':
        # for method == 'GET':
        valid = True

        if request.args.get('seed'):
            seed = request.args.get('seed')
        else:
            valid = False
            seed = random_string(10)

        if request.args.get('race_choice') \
                and npc_generator.validate_params(race_choice=request.args.get('race_choice')):
            race_choice = request.args.get('race_choice')
        else:
            valid = False
            race_choice = npc_generator.get_random_option('race')

        if request.args.get('class_choice') \
                and npc_generator.validate_params(class_choice=request.args.get('class_choice')):
            class_choice = request.args.get('class_choice')
        else:
            valid = False
            class_choice = npc_generator.get_random_option('class')

        if request.args.get('hd') \
                and npc_generator.validate_params(hd=request.args.get('hd')):
            hd = int(request.args.get('hd'))
        else:
            valid = False
            hd = random.randint(1, 20)

        if not valid:
            return redirect(url_for('npc', seed=seed, hd=str(hd),
                                    race_choice=race_choice, class_choice=class_choice, ))

    new_npc = npc_generator.new_character(
        race_template_name=race_choice,
        class_template_name=class_choice,
        seed=seed,
        hit_dice_num=hd,
    )

    stat_block = new_npc.build_stat_block()
    plaintext = stat_block.plain_text()
    stat_block_dict = stat_block.get_dict()

    html_traits = []
    for entry in stat_block_dict['passive_traits']:
        html_traits.append((entry[0], entry[1].replace("\n", "<br/>")))
    stat_block_dict['passive_traits'] = html_traits

    race_options = npc_generator.get_options('race')
    class_options = npc_generator.get_options('class')
    hd_range = list(range(1, 21))
    return render_template('npc.html',
                           seed=seed,
                           stat_block=stat_block_dict,
                           race_options=race_options,
                           race_choice=race_choice,
                           class_options=class_options,
                           class_choice=class_choice,
                           hd_range=hd_range,
                           hd=str(hd),
                           plaintext=plaintext)
