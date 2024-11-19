[![Slack](https://img.shields.io/badge/slack-join-blue.svg)](https://xcyber360.com/community/join-us-on-slack/)
[![Email](https://img.shields.io/badge/email-join-blue.svg)](https://groups.google.com/forum/#!forum/xcyber360)
[![Documentation](https://img.shields.io/badge/docs-view-green.svg)](https://documentation.xcyber360.com)
[![Documentation](https://img.shields.io/badge/web-view-green.svg)](https://xcyber360.com)
[![Twitter](https://img.shields.io/twitter/follow/xcyber360?style=social)](https://twitter.com/xcyber360)
[![YouTube](https://img.shields.io/youtube/views/peTSzcAueEc?style=social)](https://www.youtube.com/watch?v=peTSzcAueEc)


# Xcyber360 QA framework

This repository contains a toolset so that the tests and developers can build tests in a modular and efficient way.

## How to install

>Note: As precondition, you must have installed a python version >=3.8.0

First, you have to install the python dependencies. These dependencies are needed to use and import the repository framework tools. You can install them using the `requirements.txt` file that is located in the root path of this repository:

```
python3 -m pip install -r requirements.txt
```

Next, you have to install the `xcyber360-qa-framework` in order to use it as python dependency. To do this, you have to install the `setup.py` file that is located in the root path of this repository.

```
python3 setup.py install
```

## How to use

Once you have installed the `xcyber360-qa-framework`, you can use and import it into your python scripts or tests modules.

```
from xcyber360_qa_framework.x import y
```

