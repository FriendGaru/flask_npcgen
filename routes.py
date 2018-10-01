from flask import Flask, url_for, request, render_template
from app import app
import npcgen.npcgen

npc_generator = None

@app.route('/')
def hello():
    return 'hello'

@app.route('/test')
def test():
    global npc_generator
    if not npc_generator:
        npc_generator = npcgen.npcgen.NPCGenerator()
    npc = npc_generator.new_character()
    stat_block = npc.build_stat_block()
    return stat_block.display()
