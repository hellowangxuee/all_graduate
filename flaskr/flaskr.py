# -*- coding: utf-8 -*-
"""
    Flaskr
    ~~~~~~

    A microblog example application written as Flask tutorial with
    Flask and sqlite3.

    :copyright: (c) 2015 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import networkx as nx
import community
import json
from networkx.readwrite import json_graph
import his
import icc
import bicc
import wx


# create our little application :)
app = Flask(__name__)
graph = {}
area = []
edge = 0

#生成图结构，并存储到json文件中
G = nx.relaxed_caveman_graph(10, 10, 0.1, seed=42)
partition = community.best_partition(G)
for n in G:
    G.node[n]['name'] = n
    G.node[n]['group'] = partition[n]
    graph[n] = []
    for k, v in G.edge[n].items():
        graph[n].append(k)
        edge += 1
    area.append(partition[n])
d = json_graph.node_link_data(G)
json.dump(d, open('static/force/community_Picture.json', 'w'))

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()



@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    #return render_template('show_entries.html', entries=entries)
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
               [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/first')
def first():
    return render_template('first.html')

@app.route('/algorithmHIS')
def algorithmHIS():
    His = his.HIS(graph, area, edge)
    list = His.structure_hole_min_max_faster(10)
    for n in G:
        if n in list:
            G.node[n]['group'] = 1
        else:
            G.node[n]['group'] = 0
    d = json_graph.node_link_data(G)
    json.dump(d, open('static/force/his.json','w'))
    return render_template('algorithmHIS.html')

@app.route('/algorithmICC')
def algorithmICC():
    ICc = icc.ICC(graph, edge)
    list = ICc.algorithmICC(10)
    for n in G:
        if n in list:
            G.node[n]['group'] = 1
        else:
            G.node[n]['group'] = 0
    d = json_graph.node_link_data(G)
    json.dump(d, open('static/force/icc.json','w'))
    return render_template('algorithmICC.html')

@app.route('/algorithmBICC')
def algorithmBICC():
    BIcc = bicc.BICC(graph, edge)
    list = BIcc.algorithmBICC(10, 2*10, 2)
    for n in G:
        if n in list:
            G.node[n]['group'] = 1
        else:
            G.node[n]['group'] = 0
    d = json_graph.node_link_data(G)
    json.dump(d, open('static/force/bicc.json','w'))
    return render_template('algorithmBICC.html')

@app.route('/algorithmWX')
def algorithmWX():
    WX = wx.wx(graph, area, edge)
    list = WX.algorithmWX(10, 2)
    for n in G:
        if n in list:
            G.node[n]['group'] = 1
        else:
            G.node[n]['group'] = 0
    d = json_graph.node_link_data(G)
    json.dump(d, open('static/force/wx.json','w'))
    return render_template('algorithmWX.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            #return redirect(url_for('show_entries'))
            return redirect(url_for('first'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run()