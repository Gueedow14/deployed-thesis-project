# Personalized Anonymization of Knowledge Graphs Website

A web application for personalized anonymization of knowledge graphs.

## Quick Setup

### Anaconda

Setup the python virtual environment using Anaconda.

Follow the instructions to install Anaconda [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

Verify that conda is installed and running on your system by typing:

```bash
conda --version
```

After installing Conda create a virtual environment that contains Python 3.9.

```bash
conda create --name virtual_env python=3.9
```

Activate the conda virtual environment newly created.

```bash
conda activate virtual_env
```

The active environment is also displayed in front of your prompt in (parentheses) or [brackets] like this:

```bash
(virtual_env) $
```

If no virtual environment is active then this will be seen on screen:

```bash
(base) $
```

Now you're ready to progress with the setup process. If you'd like to exit the current virtual environment you're using simply type:

```bash
conda deactivate
```

### Python

Check if python is installed using the following command

```bash
python --version
```

If an error is raised it means you need to [install Python](https://www.python.org/downloads/).

### Pip

Check if package manager pip is installed by typing:

```bash
pip --version
```

If an error is raised it means you need to [install Pip](https://pip.pypa.io/en/stable/installation/).

### Install the required packages

To initialize the repository, please install all packages stored in file `requirements.txt`.

```bash
conda install --name virtual_env --file "requirements.txt"
```

If some of the packages are unavailable through conda, try finding and installing them with [conda-forge](https://conda-forge.org/docs/) or you can manually install them using pip command.

```bash
pip install <PACKAGE>==<VERSION>
```

## Post-Installation Guideline

In order to execute the program correctly it's suggested that you change the `base_dir` variable in the `views.py` file.

You can find the variable at lines: 1647, 1789, 1943.
Set it to the path of the folder containing the `manage.py` file.


## Run Locally

Using the command prompt move into the folder that contains the `manage.py` file (named kg-anonymization) and run the following command:

```bash
python manage.py runserver
```
Now you can run the program locally by typing `localhost:8000/anon/logreg` in your browser.

## Work with the Anonymized Graph file

When you're anonymizing a knowledge graph you can choose whether or not to download a file that represents the anonymized graph.
The file is a .ttl file, which is the file extension used for [Turtle Graphics Data Format files](https://en.wikipedia.org/wiki/Turtle_(syntax)).

Here are some useful links:
- [Validate .ttl file](http://ttl.summerofcode.be/)
- [Convert the file to another format](https://www.easyrdf.org/converter)
- [Visualize Anonymized Graph](https://www.ldf.fi/service/rdf-grapher)




# Video Tutorial


https://user-images.githubusercontent.com/51020750/220290185-3918e5c5-da77-48c1-91d5-d6e15ec8ff6d.mp4