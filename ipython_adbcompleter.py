"""IPython completer for adb commands.

To activate, pip-install and append the output of `ipython -m ipython_adbcompleter`
to `~/.ipython/profile_default/ipython_config.py`.
"""
import os
import subprocess


try:
    import _ipython_adbcompleter_version
except ImportError:
    from pip._vendor import pkg_resources
    __version__ = pkg_resources.get_distribution("ipython-adbcompleter").version
else:
    __version__ = _ipython_adbcompleter_version.get_versions()["version"]


def adb_completer(self, event):
    """
    A simple completer that returns the arguments that adb accepts
    """
    subs = event.text_until_cursor[event.text_until_cursor.find('adb ') + 4:]

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
    """
    Replacement glob that also searches on connected device

    The path must start with '/'.
    """
    paths = list(_original_glob(pathname))

    if _enabled and pathname.endswith('*') and pathname.startswith('/'):
        pathname = pathname[:-1]
        pathbase = pathname[:pathname.rfind('/')]
        filename = pathname[pathname.rfind('/') + 1:]

        try:
            files = subprocess.check_output('adb shell ls %s' % pathbase, shell=True, stderr=subprocess.STDOUT).splitlines()
            if len(files) > 1 or (files[0] != 'error: device not found' and files[0] != "opendir failed, Permission denied" and not files[0].endswith('No such file or directory')):
                paths.extend(pathbase + '/' + f for f in files if f.startswith(filename))
        except Exception:
            pass

    return paths


if __name__ != "__main__":
    from IPython.core.magic import register_line_magic

    @register_line_magic
    def adb(arg):
        """Conveniance magic for running adb"""
        os.system('adb %s' % arg)


def load_ipython_extension(ipython):
    """
    Load the extension.

    This replace the default completer's `glob` reference with a function that also searches on a connected device.
    """
    global _original_glob, _enabled
    _enabled = True
    _original_glob = ipython.Completer.glob
    ipython.Completer.glob = adb_glob
    ipython.set_hook('complete_command', adb_completer, re_key='.*adb ')


def unload_ipython_extension(ipython):
    """
    Unload the extension

    We can't just replace the glob function back, since maybe someone else replaced the glob after us. So we just disable the adb part.
    """
    global _original_glob, _enabled
    _enabled = False


if __name__ == "__main__":
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
