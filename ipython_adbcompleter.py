"""IPython completer for adb commands.

To activate, pip-install and append the output of `ipython -m ipython_adbcompleter`
to `~/.ipython/profile_default/ipython_config.py`.
"""
import os
import re
import subprocess


try:
    import _ipython_adbcompleter_version
except ImportError:
    from pip._vendor import pkg_resources
    __version__ = pkg_resources.get_distribution("ipython-adbcompleter").version
else:
    __version__ = _ipython_adbcompleter_version.get_versions()["version"]


def slash_chr(s, c):
    sc = '\\%c' % c
    return sc.join(ss.replace(c, sc) for ss in s.split(sc))

def unslash_chr(s, c):
    sc = '\\%c' % c
    while True:
        s2 = s.replace(sc, c)
        if s != s2:
            return s2
        s = s2


def adb_completer(self, event):
    """
    A simple completer that returns the arguments that adb accepts
    """
    adb_completer.event = event
    subs = event.text_until_cursor[event.text_until_cursor.find('adb ') + 4:]

    if re.match(r"(^|^.*\s)-s\s+[^\s]*$", subs):
        return adb_devices()
    elif re.match(r"^(-s [^\s]*\s+)?[^\s]*$", subs):
        return [
            '-a',
            '-d',
            '-e',
            '--help',
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

    pathname = None

    for nr, pattern, in_quotes in [
        (3, r"^(-s ([^\s]*)\s+)?pull\s+(([^\s\"']|(?<=\\)[ \"'])*)$", False),
        (3, r"^(-s ([^\s]*)\s+)?pull\s+\"(([^\"]|(?<=\\)\")*)$", True),
        (5, r"^(-s ([^\s]*)\s+)?push\s+\"(([^\"]|(?<=\\)\")*)\"\s+(([^\s\"']|(?<=\\)[ \"'])*)$", False),
        (5, r"^(-s ([^\s]*)\s+)?push\s+(([^\s\"']|(?<=\\)[ \"'])*)\s+(([^\s\"']|(?<=\\)[ \"'])*)$", False),
        (5, r"^(-s ([^\s]*)\s+)?push\s+(([^\s\"']|(?<=\\)[ \"'])*)\s+\"(([^\"]|(?<=\\)\")*)$", True),
        (5, r"^(-s ([^\s]*)\s+)?push\s+\"(([^\"]|(?<=\\)\")*)\"\s+\"(([^\"]|(?<=\\)\")*)$", True)
        ]:
        m = re.match(pattern, subs)
        if m:
            pathname = m.group(nr)
            res = [slash_chr(slash_chr(slash_chr(s, '"'), "'"), ' ') for s in parse_and_ls(pathname, m.group(1))]

            if not in_quotes:
                res = [slash_chr(s, ' ') for s in res]

            return [p[len(pathname) - len(event.symbol):] for p in res]
    
    return []


_enabled = False


def parse_and_ls(pathname, device):
    if pathname.endswith('/'):
        return shell_ls(pathname, '', device)
    else:
        last_slash = pathname.rfind('/')
        if last_slash == -1:
            return [f[1:] for f in shell_ls('/', pathname, device)]
        else:
            return shell_ls(pathname[:pathname.rfind('/') + 1], pathname[pathname.rfind('/') + 1:], device)


def shell_ls(pathbase, filename, device):
    if device is None:
        device = ''
    try:
        files = subprocess.check_output('adb %sshell ls "%s"' % (device, pathbase), shell=True, stderr=subprocess.STDOUT).splitlines()
    except Exception:
        return []
    
    paths = []
    if (len(files) > 1 or 
        (len(files) == 1 and files[0] != 'error: device not found' and 
            files[0] != "opendir failed, Permission denied" and 
            not files[0].endswith('No such file or directory'))):
        for f in files:
            try:
                if f.startswith(filename):
                    paths.append('%s%s%s' % (pathbase, '' if pathbase.endswith('/') else  '/', f))
            except Exception:
                pass

    return paths


def adb_devices():
    try:
        lines = [line for line in subprocess.check_output('adb devices', shell=True, stderr=subprocess.STDOUT).splitlines() if line]
    except Exception:
        return []

    if len(lines) <= 1 or lines[0] != 'List of devices attached':
        return []

    lines = lines[1:]
    devices = [line.split()[0] for line in lines]

    return devices


if __name__ != "__main__":
    from IPython.core.magic import register_line_magic

    @register_line_magic
    def adb(arg):
        """Conveniance magic for running adb"""
        os.system('adb %s' % arg)


def load_ipython_extension(ipython):
    """
    Load the extension.
    """
    global _enabled
    _enabled = True
    ipython.set_hook('complete_command', adb_completer, re_key='.*adb ')


def unload_ipython_extension(ipython):
    """
    Unload the extension
    """
    global _enabled
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
