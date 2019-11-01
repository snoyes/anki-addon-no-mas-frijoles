This repo is an example of using 3rd party modules to support your Anki add-on.

Here's one way to do it:

Set up a virtual environment, so any modules you download don't go into your global space:
```
python -m venv .venv
.venv\Scripts\activate
```

Grab the modules you want:
`pip install googletrans`

You can exit the virtual environment now:
`deactivate`

Copy .venv\Lib\site-packages\googletrans to your add-on folder.

Within your add-on's code, e.g. in __init__.py, adjust the path so that the import will look in the correct directory for the module.

```
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
```

Now you can import it, e.g.
`from googletrans import Translator`

