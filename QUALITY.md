# Quality

## Hooks

- A pre-commit hook should be installed to automatically format files on commit with the following command:

  ```shell
  pre-commit install
  ```

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

## Code

- [Black](https://github.com/psf/black) should be used to format the code:

  ```shell
  black gtagger.py src
  ```

- [Pylint](https://github.com/PyCQA/pylint) should be used to lint the code (some warnings are disabled):

  ```shell
  pylint gtagger.py src  --max-line-length=120 --disable R0902 --disable R0903 --disable R0904 --disable R0911 --disable R0913 --disable R0914 --disable R0915 --disable I1101
  ```

## Docstrings

Docstrings follow the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html).

- [darglint](https://github.com/terrencepreilly/darglint) should be used to lint the content of the docstrings:

  ```shell
  darglint gtagger.py src
  ```

- [pydocstyle](https://github.com/PyCQA/pydocstyle) should be used to lint the formatting of the docstrings:

  ```shell
  pydocstyle gtagger.py src
  ```
