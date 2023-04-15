
# Codetronaut

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](http://forthebadge.com)
[![forthebadge](http://forthebadge.com/images/badges/built-with-love.svg)](http://forthebadge.com)
---
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=shields)](http://makeapullrequest.com)

Codetronaut is a voice assistant that allows developers to code without ever touching the keyboard. Using a very generic implementation, Codetronaut allows any IDE, language, or platform to work. While it has working features already, Codetronaut is in its early stages of development, so the only working IDE at the moment is Visual Studio Code, and the only current programming language is Java. Here's a glimpse!

 https://user-images.githubusercontent.com/38501844/231871582-2391bd56-6a34-4384-ab7b-87fc1e7d1125.mp4

# Table of contents

- [Setting up](#setting-up)
- [Getting started](#getting-started)
- [Contributing](#contributing)
- [License](#license)

# Setting up

[(Back to top)](#table-of-contents)

1. [Download](https://www.python.org/downloads/release/python-390/) and install Python3.9.
2. [Download](https://ffmpeg.org/) FFmpeg, and add the `bin` folder to your Path environment variable.
3. [Download](https://github.com/ismyilson/Codetronaut/archive/refs/heads/main.zip) or clone this repository and install the package requirements with:
    ```
    pip install -r requirements.txt
    ```
4. Run `python -m app` to start using Codetronaut!

# Getting started

[(Back to top)](#table-of-contents)

Some commands are used for configuration, and due to their nature might require a couple clicks (don't worry, these are the only times you'll click!), that being said, some useful commands to get started are:
- `Set work directory`. This will show a popup window asking you to select a directory, which will be marked as work directory.
-  `Set editor to <editor of choice>`. This will set the editor (and start it) to your editor of choice.*

<sub>*Currently, due to Codetronaut being in its very early stages of development, the only supported editor is Visual Studio Code, you can use `Set editor to visual studio code` to set it. </sub>

# Contributing

[(Back to top)](#table-of-contents)

Your contributions are always welcome!

# License

[(Back to top)](#table-of-contents)

Codetronaut is under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/deed.en). Please have a look at the [LICENSE.md](LICENSE.md) for more details.
