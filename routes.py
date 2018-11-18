from flask import Flask, url_for, request, render_template, redirect
import random
import string
from flask_npcgen import app
from npcgen.npcgen import npcgen_main

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
    global character_build_options
    if not npc_generator:
        print("NPCGenerator not found, building new one.")
        npc_generator = npcgen_main.NPCGenerator()

    if not request.method == 'GET':
        return redirect(url_for('npc',))

    validity, clean_request = npc_generator.validate_request_dict(request.args)

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

    fresh_seed = random_string(10)

    return render_template('main.html',
                           build_options_json=npc_generator.build_options_json,
                           build_options=npc_generator.content_source.build_options_dict,
                           fresh_seed=fresh_seed,
                           stat_block=stat_block_dict,
                           plaintext=plaintext,
                           npc_request=clean_request,
                           )
