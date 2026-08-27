# teesh

tee for python subprocess

[![version](https://img.shields.io/pypi/v/teesh.svg)](https://pypi.org/project/teesh)
[![license](https://img.shields.io/pypi/l/teesh.svg)](https://github.com/amyreese/teesh/blob/main/LICENSE)


teesh is a streamlined, modern interpretation of `subprocess.run()`, with an API
inspired by the needs of human-focused automation and scripts.

When running a subprocess with teesh, stdout and stderr will always be captured,
but stdout and stderr will also always go to the console, allowing both the user
and the program to see and introspect the output:

```pycon
>>> import teesh
>>> result = teesh.run("/bin/echo", "hello world")
hello world
>>> # ^ this message was sent to stdout
>>> # v it was also captured in the result
>>> result
CompletedProcess(cmd=('/bin/echo', 'hello world'), returncode=0, stdout='hello world\n', stderr='')
```

teesh checks for non-zero return codes by default:

```pycon
>>> teesh.run("/usr/bin/false")
Traceback (most recent call last):
  ...
teesh.core.CalledProcessError: Command '/usr/bin/false' returned non-zero exit status 1.
```

teesh always uses unicode strings instead of bytes:

```pycon
>>> type(teesh.run("/bin/echo", "hello world").stdout)
hello world
<class 'str'>
```

teesh happily accepts mixed `Path` objects:

```pycon
>>> filename = Path("README.md")
>>> teesh.run("head", "-n1", filename)
# teesh
CompletedProcess(cmd=('head', '-n1', 'README.md'), returncode=0, stdout='# teesh\n', stderr='')
```

teesh is composable:

```pycon
>>> from functools import partial
>>> sudo = partial(teesh.run, "sudo")
>>> sudo("whoami")
root
CompletedProcess(cmd=('sudo', 'whoami'), returncode=0, stdout='root\n', stderr='')
```

License
-------

teesh is and always will be 100% human generated.

teesh is copyright Amethyst Reese, and licensed under the MIT license.
