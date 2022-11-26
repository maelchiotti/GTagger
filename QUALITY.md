# Code quality

## Stubs

Stubs should be generated with the following commands:

- PySide6:

```shell
pyside6-genpyi all
```

- Other packages:

```shell
stubgen -p mutagen -p genius -p qdarktheme -p qtawesome -p regex -o stubs
```

## Pylint

[Pylint](https://pylint.pycqa.org/en/latest/) should be used with the following command:

```shell
pylint gtagger.py src --disable R0902 --disable R0903 --disable R0904 --disable R0913 --disable R0914 --disable R0915 --disable I1101
```
