# ipython-adbcompleter
An IPython completer for adb commands

Beyond the basic argument completion, this extension also adds completions for file/directory paths:

```
In [1]: adb p  # hit tab!
pull
push
In [1]: adb pull /storage/  # hit tab!
6432-6235
emulated
enc_emulated
Private
self
In [1]: adb pull /storage/emu  # hit tab!
In [1]: adb pull /storage/emulated
```

Amazing! This will save me so much time!

Notes:
1. The android path must start with `/`. This is to reduce queries to the phone when you want a path on your computer.
2. Unicode characters in paths mess up my ipython, so for now adbcompleter just skips them.
3. adbcompleter currently only supports a single connected device.

# Install
Use pip like this:
`pip install git+https://github.com/drorspei/ipython-adbcompleter`

Then add the following lines to your `ipython_config.py` file (usually in `~/.ipython/profile_default/`):
```
c.InteractiveShellApp.exec_lines.append(
    "try:\n    %load_ext ipython_adbcompleter\nexcept ImportError: pass")
```
