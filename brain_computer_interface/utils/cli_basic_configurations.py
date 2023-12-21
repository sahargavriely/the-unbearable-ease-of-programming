import os
import sys
import traceback

import click

import brain_computer_interface


class Log:

    def __init__(self):
        self.quiet = False
        self.traceback = False

    def __call__(self, message):
        if self.quiet:
            return
        if self.traceback and sys.exc_info():  # there's an active exception
            trace = traceback.format_exc().strip()
            if trace != 'NoneType: None':
                message = message or ''
                message += os.linesep + trace
        click.echo(message)


log = Log()


@click.group(context_settings={'show_default': True})
@click.version_option(brain_computer_interface.version)
@click.option('-q', '--quiet', is_flag=True)
@click.option('-t', '--traceback', is_flag=True)
def main(quiet=False, traceback=False):
    log.quiet = quiet
    log.traceback = traceback


@main.command('error')
def error_():
    raise RuntimeError('something went terribly wrong :[')


def module_main_exe(*submodules_names):
    names = ['brain_computer_interface']
    for submodule_name in submodules_names:
        names.append(submodule_name)
    try:
        main(prog_name='.'.join(names))
    except Exception as error:
        log(f'ERROR: {error}')
        sys.exit(1)
