'''
CLI program that will connect to the web server and actually play the music
Also must manage the queue
'''
from os import environ
import sys
import click
import requests
from listener import poll_and_wait


def get_server():
    ''' Get environment variable or raise an error '''
    server_add = environ.get('SERVER_ADDR', False)
    if not server_add:
        click.echo('Missing environment variable for server address', err=True)
        click.echo('Set env var SERVER_ADDR and try again', err=True)
        sys.exit()
    if 'http://' not in server_add:
        server_add = 'http://{}'.format(server_add)
    return server_add


@click.group()
def cli():
    ''' Manage connections with the ScHoolboy Queue web app '''
    pass

@click.command()
def create():
    '''
    Create a new room without attaching to it
    '''
    server_add = get_server()
    endpoint = '{}/room/new/'.format(server_add)
    resp = requests.post(endpoint)
    click.echo(resp.json())


@click.command()
@click.argument('room')
def delete(room):
    '''
    Delete a previously created room for housekeeping reasons
    '''
    server_add = get_server()
    endpoint = '{}/room/delete/'.format(server_add)
    resp = requests.post(endpoint, data={'room': room})
    click.echo(resp.json())

@click.command()
@click.option('--room', default=False,
              help='Connect to an already existing room id')
def connect(room):
    '''
    Connect to the webapp and start playing music
    '''
    server_add = get_server()
    if room:
        click.echo(room)
    else:
        endpoint = '{}/room/new/'.format(server_add)
        resp = requests.post(endpoint)
        click.echo(resp.json())
        room = resp.json()['room']
    poll_and_wait(room, 5, server_add)



cli.add_command(connect)
cli.add_command(create)
cli.add_command(delete)
