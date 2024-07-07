# Lecturemd

A system for generating lecture notes and slides from a single markdown file, for both HTML and PDF output.

## Requirements

- [Python 3](https://www.python.org/), version 3.8 or later (the more recent the better)
- [Pandoc](https://pandoc.org/)
- For Linux: [pdf2svg](https://github.com/dawbarton/pdf2svg)
- For Windows: [Inkscape](https://inkscape.org/)
- [ImageMagick](https://imagemagick.org/index.php)
- [LaTeX](https://www.latex-project.org/), specifically `pdflatex`
- [LaTeXmk](https://ctan.org/pkg/latexmk/?lang=en) 

### Python Packages

- [Pygmentation](https://github.com/ech0-chambers/pygmentation)
- [Pyndoc](https://github.com/ech0-chambers/pyndoc) (Not strictly required but highly recommended)
- [Panflute](https://github.com/sergiocorreia/panflute)
- [Pyaml](https://pyyaml.org/)
- [Textual](https://github.com/Textualize/textual)
- [Pint](https://pint.readthedocs.io/en/stable/)

## Installation

### Linux

1. Check your Python version with
    ```bash
    python3 --version
    ```
    At least version 3.8 is required, but more recent versions are recommended. If needed, update your Python version with your package manager. For example, on Ubuntu or other Debian-based systems, you can update Python with
    ```bash
    sudo apt update
    sudo apt install --only-upgrade python3
    ```
1. Install the required packages with
    ```bash
    sudo apt install pandoc pdf2svg imagemagick
    ```
1. The recommended installation of LaTeX is [TeX Live](https://www.tug.org/texlive/). This installation can take a long time, especially on slower internet connections. To install TeX Live, run
    ```bash
    sudo apt install texlive-full
    ```
1. Install Pyndoc by following the instructions in the [Pyndoc README](https://github.com/ech0-chambers/pyndoc/blob/main/README.md#installation).
1. Install Pygmentation by following the instructions in the [Pygmentation README](https://github.com/ec0-chambers/pygmentation/blob/main/README.md#installation).
1. Install this package
    1. Download this repository and extract it.
    1. Navigate to the extracted directory in your terminal. For example,
        ```bash
        cd ~/Downloads/lecturemd-main/lecturemd-main
        ```
    1. Navigate to the `src` directory
        ```bash
        cd src
        ```
    1. If you would like to, run
        ```bash
        python3 check_requirements.py
        ```
        to ensure that all required packages are installed and available.
    1. Install the package with
        ```bash
        pip install .
        ```
    1. Verify the installation by running
        ```bash
        lecturemd --help
        ```

### Windows

The recommended route for installing the requirements is to use the chocolatey package manager. If you do not wish to use chocolatey, all required packages can be installed manually. However, when installing Inkscape manually, you *must* ensure that the Inkscape executable is in your system's PATH. During installation, ensure that the option "Add Inkscape to the system PATH for all users" is selected.


1. It is optional but highly encouraged to install the Windows Terminal from the Microsoft Store. This terminal provides drastically a better experience than the default Command Prompt.
1. Install Chocolatey by following the instructions at [chocolatey.org](https://chocolatey.org/install).
1. Open a command prompt with administrator privileges.
1. Install the required packages with
    ```cmd
    choco install python pandoc imagemagick inkscape miktex latexmk
    ```
1. Open the start menu and search for "App Execution Aliases". <!-- TODO: Finish this instruction step. --->
1. Open a new command prompt with administrator privileges.
1. Verify that Python has been correctly installed by running
    ```cmd
    python --version
    ```
    The output should be the version of Python that you installed. If instead the Microsoft Store is opened, refer to step 5.
1. Install Pyndoc by following the instructions in the [Pyndoc README](https://github.com/ech0-chambers/pyndoc/blob/main/README.md#installation).
1. Install Pygmentation by following the instructions in the [Pygmentation README](https://github.com/ec0-chambers/pygmentation/blob/main/README.md#installation).
1. Install the required Python packages by running
    ```cmd
    pip install pyaml panflute textual pint
    ```
1. Install this package
    1. Download this repository and extract it.
    1. Navigate to the extracted directory in your terminal. For example,
        ```cmd
        cd C:\Users\username\Downloads\lecturemd-main\lecturemd-main
        ```
    1. Navigate to the `src` directory
        ```cmd
        cd src
        ```
    1. If you would like to, run
        ```cmd
        python check_requirements.py
        ```
        to ensure that all required packages are installed and available.
    1. Install the package with
        ```cmd
        pip install .
        ```
    1. Verify the installation by running
        ```cmd
        lecturemd --help
        ```

### MacOS

*Instructions coming soon.*

## Usage

### Creating a New Lecture

To create a new lecture series, open a terminal/command prompt and navigate to the directory where you would like to create the lecture series. Run the following command:

```bash
lecturemd new your_lecture_name
```
replacing `your_lecture_name` with the name of your lecture series. This command will create a new directory with the name you provided, and populate it with the necessary files and directories.

If the directory already exists, the you will be asked for confirmation to overwrite the existing directory. You can use the option `--overwrite` or `-o` to automatically overwrite the existing directory without confirmation, or `--non-interactive` or `-I` to fail if the directory already exists.

You can also pass the option `--configure` or `-c` to immediately configure the lecture series after creating it. This is equivalent to running
```bash
lecturemd new your_lecture_name
cd your_lecture_name
lecturemd configure
```
See the section on [Configuring a Lecture Series](#configuring-a-lecture-series) for more information.

### Configuring a Lecture Series

To configure a lecture series, navigate to the root directory of the lecture series (this will usually be the directory containing the file `main.md`) and run the following command:

```bash
lecturemd configure
```

This will start an interactive app in the terminal where you can configure the lecture series. Alternatively, you can directly modify the file `.lecturemd/lecturemd.yaml` in the root directory of the lecture series. 

### Building the Lecture

To build the notes and slides in pdf and web format, navigate to the root directory of the lecture series and run the following command:

```bash
lecturemd build all
```

Alternatively, you can specify which output formats are built. For example, to build both notes and slides in pdf format, run

```bash
lecturemd build pdf
```

To build only the slides in web format, run

```bash
lecturemd build web slides
```

See `lecturemd build --help` for more all options.