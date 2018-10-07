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
    return redirect(url_for('npc'))

@app.route('/')
def test():
    return "Server is up."


@app.route('/npc', methods=['GET'])
def npc():
    global npc_generator
    if not npc_generator:
        npc_generator = genny.NPCGenerator()

    # seed = ''
    # hd_num_choice = 0
    # hd_size_choice = 0
    # class_choice = 'NO CLASS CHOICE!!!'
    # race_choice = 'NO_RACE_CHOICE'
    # attribute_roll_method_choice = 'NO ATTRIBUTE ROLL METHOD'

    if not request.method == 'GET':
        return redirect(url_for('npc',))
        # for method == 'GET':
        # valid = True
        #
        # if request.args.get('seed'):
        #     seed = request.args.get('seed')
        # else:
        #     valid = False
        #     seed = random_string(10)
        #
        # if request.args.get('race_choice') \
        #         and npc_generator.validate_params(race_choice=request.args.get('race_choice')):
        #     race_choice = request.args.get('race_choice')
        # else:
        #     valid = False
        #     race_choice = npc_generator.get_random_option('race')
        #
        # if request.args.get('class_choice') \
        #         and npc_generator.validate_params(class_choice=request.args.get('class_choice')):
        #     class_choice = request.args.get('class_choice')
        # else:
        #     valid = False
        #     class_choice = npc_generator.get_random_option('class')
        #
        # if request.args.get('attribute_roll_method_choice') \
        #         and npc_generator.validate_params(roll_choice=request.args.get('attribute_roll_method_choice')):
        #     attribute_roll_method_choice = request.args.get('attribute_roll_method_choice')
        # else:
        #     valid = False
        #     attribute_roll_method_choice = '3d6'
        #
        # if request.args.get('hd_num_choice') \
        #         and npc_generator.validate_params(hd=request.args.get('hd_num_choice')):
        #     hd_num_choice = int(request.args.get('hd_num_choice'))
        # else:
        #     valid = False
        #     hd_num_choice = random.randint(1, 20)
        #
        # if request.args.get('hd_size_choice') \
        #         and npc_generator.validate_params(hd_size=request.args.get('hd_size_choice')):
        #     hd_size_choice = request.args.get('hd_size_choice')
        #     if hd_size_choice != 'Default':
        #         hd_size_choice = int(request.args.get('hd_size_choice'))
        # else:
        #     valid = False
        #     hd_size_choice = 'Default'

    print(request.args)

    # new_character_request = {}
    # new_character_request['race_choice'] = request.args.get('race_choice', None)
    # new_character_request['class_choice'] = request.args.get('class_choice', None)
    # new_character_request['hit_dice_num'] = request.args.get('hit_dice_num', None)
    # new_character_request['seed'] = request.args.get('seed', None)
    # new_character_request['hit_dice_size'] = request.args.get('hit_dice_size', None)
    # new_character_request['attribute_roll_method'] = request.args.get('attribute_roll_method', None)

    validity, clean_request = npc_generator.validate_request_dict(request.args)

    print(clean_request)

    if not validity:
        return redirect(url_for('npc', **clean_request))

    new_npc = npc_generator.new_character(**clean_request)

    stat_block = new_npc.build_stat_block()
    plaintext = stat_block.plain_text()
    stat_block_dict = stat_block.get_dict()

    html_passive_traits = []
    for entry in stat_block_dict['passive_traits']:
        html_passive_traits.append((entry[0], entry[1].replace("\n", "<br/>")))
    stat_block_dict['passive_traits'] = html_passive_traits

    html_spellcasting_traits = []
    for entry in stat_block_dict['spellcasting_traits']:
        html_spellcasting_traits.append((entry[0], entry[1].replace("\n", "<br/>")))
    stat_block_dict['spellcasting_traits'] = html_spellcasting_traits

    # race_options = npc_generator.get_options('race')
    # class_options = npc_generator.get_options('class')
    # hd_num_options = [(str(x), str(x)) for x in range(1, 21)]
    # # hd_size_options = [(4, 4), (6, 6), (8, 8), (10, 10), (12, 12)]
    # hd_size_options = [(str(x), str(x))for x in npc_generator.hd_size_options]
    # print(hd_size_options)
    # attribute_roll_method_options = npc_generator.roll_options

    form_options = npc_generator.get_options_dict()

    fresh_seed = random_string(10)

    return render_template('main.html',
                           fresh_seed=fresh_seed,
                           stat_block=stat_block_dict,
                           plaintext=plaintext,
                           npc_request=clean_request,
                           form_options=form_options,)
