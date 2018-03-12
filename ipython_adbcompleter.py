"""IPython completer for adb commands.

To activate, pip-install and append the output of `ipython -m ipython_adbcompleter`
to `~/.ipython/profile_default/ipython_config.py`.
"""
import os
import re
import subprocess
from glob import glob
from IPython.core.magic import register_line_magic


try:
    import _ipython_adbcompleter_version
except ImportError:
    from pip._vendor import pkg_resources
    __version__ = pkg_resources.get_distribution("ipython-adbcompleter").version
else:
    __version__ = _ipython_adbcompleter_version.get_versions()["version"]


def protect_filename(txt):
    return txt.replace(" ", "\\ ")


def adb_completer(self, event):
    subs = event.text_until_cursor[event.text_until_cursor.find('adb ') + 4:]   # type: str

    if ' ' not in subs:
        return [
            '-a',
            '-d',
            '-e',
            '-s',
            '-p',
            '-H',
            '-P',
            'devices',
            'connect',
            'disconnect',
            'push',
            'pull',
            'sync',
            'shell',
            'emu',
            'logcat',
            'forward',
            'reverse',
            'jdwp',
            'install',
            'uninstall',
            'bugreport',
            'backup',
            'restore',
            'help',
            'version',
            'wait-for-device',
            'start-server',
            'kill-server',
            'get-state',
            'get-serialno',
            'get-devpath',
            'status-window',
            'remount',
            'reboot',
            'reboot-bootloader',
            'root',
            'usb',
            'tcpip',
            'ppp',
        ]
    else:
        return []


_original_glob = None
_enabled = False


def adb_glob(pathname):
    paths = list(_original_glob(pathname))

    if _enabled and pathname.endswith('*') and pathname.startswith('/'):
        pathname = pathname[:-1]
        pathbase = pathname[:pathname.rfind('/')]
        filename = pathname[pathname.rfind('/') + 1:]

        files = subprocess.check_output('adb shell ls %s' % pathbase, shell=True).splitlines()
        if len(files) > 1 or (files[0] != "opendir failed, Permission denied" and not files[0].endswith('No such file or directory')):
            paths.extend(pathbase + '/' + f for f in files if f.startswith(filename))

    return paths


if __name__ != "__main__":
    @register_line_magic
    def adb(arg):
        os.system('adb %s' % arg)


def load_ipython_extension(ipython):
    """
    @type ipython: IPython.terminal.interactiveshell.TerminalInteractiveShell
    """
    global _original_glob, _enabled
    _enabled = True
    _original_glob = ipython.Completer.glob
    ipython.Completer.glob = adb_glob
    ipython.set_hook('complete_command', adb_completer, re_key='.*adb ')


def unload_ipython_extension(ipython):
    global _original_glob, _enabled
    _enabled = False


def test_adbcompleter():
    def make_event(txt):
        class event:
            text_until_cursor = txt
        return event

    print adb_completer(None, make_event("adb pull /tmp /home/"))
    print adb_completer(None, make_event("adb pull /tmp \"/home/"))
    print adb_completer(None, make_event("adb pull \"/tmp\" \"/home/"))
    print adb_completer(None, make_event("adb push \"/home/"))
    print adb_completer(None, make_event("adb push /home/"))


if __name__ == "__main__":
    # test_adbcompleter()
    import sys

    if os.isatty(sys.stdout.fileno()):
        print("""\
# Please append the output of this command to the
# output of `ipython profile locate` (typically
# `~/.ipython/profile_default/ipython_config.py`)
""")
    print("""\
c.InteractiveShellApp.exec_lines.append(
    "try:\\n    %load_ext ipython_adbcompleter\\nexcept ImportError: pass")""")
