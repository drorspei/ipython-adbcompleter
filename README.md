# ipython-adbcompleter
An IPython completer for adb commands

Beyond the basic argument completion, this extension also adds completions for file/directory paths:

```
>>> adb p  # hit tab!
pull
push
>>> adb pull /storage/  # hit tab!
6432-6235
emulated
enc_emulated
Private
self
>>> adb pull /storage/emu  # hit tab!
>>> adb pull /storage/emulated
```

Amazing! This will save me so much time!
