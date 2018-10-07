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

    form_options = npc_generator.get_options_dict()

    fresh_seed = random_string(10)

    return render_template('main.html',
                           fresh_seed=fresh_seed,
                           stat_block=stat_block_dict,
                           plaintext=plaintext,
                           npc_request=clean_request,
                           form_options=form_options,)
