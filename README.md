# Software Construction Process & Tools

<strong>Jeroen Boogaard</strong>

## Development Setup

<ol>

<li>

**Install Git**

Make sure you select "Checkout as-is, commit Unix-style line endings" during the installation process.

<ul>

<li>

[GitHub CLI](https://cli.github.com/)

</li>

<li>

(Optional) [Git Bash (Windows)](https://gitforwindows.org/)

</li>

</ul>

<li>

**Authenticate with GitHub CLI**

```sh
gh auth login
```

</li>

<li>

**Create Git Repository**

<ul>

<li>

**Create your own repository CargoHub on Github**

<p>
Browse to <a>github.com</a> and create <u>private</u> repository.
</p>

</li>

<li>

**Invite the teacher to your repository**

</li>

<li>

**Clone your git repository**

```bash
gh clone [Your_GitHub_Name]/CargoHub_[group]
```

</li>

<li>

**Configure git**

In order to commit and push your changes, you need identitify yourself.

Run the following commands from your CargoHub repo directory with your own github username and email address:

```sh
git config user.name "github_username"
git config user.email "student@hr.nl"
```

Once done, you can confirm that the information is set by running (see the last two lines):

```sh
git config --list
```
</li>

<li>

**Add, commit and push the copied contents**

<p>

Extract CargoHub.zip and add the contents to your (local) CargoHub repo

Run the following commands from your CargoHub repo directory

```sh
git add .
git commit -m "Added contents for CargoHub"
git push
```

</p>

</li>

</ul>

</li>

</ul>

</li>

<li>

**Install [Visual Studio Code](https://code.visualstudio.com)**

</li>

<li>

(Optional) Enable VSCode to be opened from the command line

Open the Command Palette and type 'shell command' in order to select the Shell command:
Install 'code' command in PATH

Start VSCode with a command from current directory

```sh
code .
```

</li>

<li>

(Optional) Install VSCode Extensions

<ul>

<li>

[Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

</li>

<li>

[Black formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)

</li>

<li>

[Git Easy extension](https://marketplace.visualstudio.com/items?itemName=bibhasdn.git-easy)

</li>

<li>

[Markdown All in One](https://marketplace.visualstudio.com/items?itemName=yzhang.markdown-all-in-one)

</li>

<li>

[Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter)

</li>

<li>

[Mermaid extension](https://marketplace.visualstudio.com/items?itemName=bierner.markdown-mermaid)

</li>

<li>

[Graphviz (dot) language support](https://marketplace.visualstudio.com/items?itemName=joaompinto.vscode-graphviz)

</li>

</ul>

</li>

</ol>


## Testing

<ol>

<li>

Install pylint

```sh
pip install pylint
```

</li>

<li>

Run pylint

```sh
pylint [python module]
```

The messages are explained at the [Pylint documentation](https://pylint.pycqa.org/en/latest/user_guide/messages/index.html")

</li>

</ol>
