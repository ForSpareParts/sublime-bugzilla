Sublime Bugzilla
================

A Sublime Text 3 plugin for interacting with the Bugzilla issue tracking
system.


Installation
------------

1. Install the ``bugzillatools`` package (``pip install bugzillatools``)
2. Clone this repository to your Sublime Text 3 ``Packages`` directory.
3. Open Preferences -> Package Settings -> Bugzilla -> Settings – User, and
edit this file to reflect your Bugzilla URL, username, and password. Use the
Bugzilla -> Settings – Default file as a model.

Now you should be good to go. If commands still don't run, find the location
of the ``bugzilla`` command (using ``which bugzilla`` from the terminal), and
use that path to populate the ``bugzilla_script`` key in your
``Bugzilla.sublime-settings``.

Commands
--------

Sublime Bugzilla adds the following commands to the Command Palette:

* **Bugzilla: Title**: Prompts for a bug number, then injects the title of the
  bug into the current buffer. Useful for including a brief bug description in
  commit messages.
  
* **Bugzilla: View Comments**: Prompts for a bug number, then opens a new buffer
  containing the complete list of comments for that bug.
  
* **Bugzilla: New Comment**: Prompts for a bug number, then opens a new buffer
  containing the complete list of comments for the bug, plus an empty space at
  the top to add a new reply to the comment thread. To submit your commment,
  close the buffer (if the comment area is empty, or contains only whitespace,
  no comment will be submitted).
