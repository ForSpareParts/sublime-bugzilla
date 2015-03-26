import sublime, sublime_plugin

import subprocess

class BugzillaIdPromptCommand(sublime_plugin.TextCommand):
    '''Gets a bug ID, then runs ``next_command``, passing in the bug ID as an
    argument.'''

    def run(self, edit, **kwargs):
        self.next_command = kwargs['next_command']
        self.use_window = kwargs.get('use_window', False)
        self.view.window().show_input_panel(
            "Bug ID:",
            "",
            self.inject,
            None,
            None)


    def inject(self, bug_id):
        if self.use_window:
            self.view.window().run_command(
                self.next_command,
                {'bug_id': bug_id})
        else:
            self.view.run_command(
                self.next_command,
                {'bug_id': bug_id})


class BugzillaInjectTextCommand(sublime_plugin.TextCommand):
    def run(self, edit, **kwargs):
        self.view.insert(edit, 0, kwargs['text'])

def bugzilla_command(command, *args):
    settings = get_settings()

    full_args = [
        '/usr/local/bin/bugzilla',
        command,
        '--url', settings.get('url'),
        '--user', settings.get('login'),
        '--password', settings.get('password')
    ]

    full_args.extend(args)

    return subprocess.check_output(
        full_args,
        stderr=subprocess.STDOUT,
        universal_newlines=True)

def get_settings():
    required_keys = ['url', 'login', 'password']
    settings = sublime.load_settings('Bugzilla.sublime-settings')

    missing_keys = []
    for key in required_keys:
        if not settings.get(key):
            missing_keys.append(key)

    if missing_keys:
        error = ('Bugzilla settings not found. Please set the folowing key(s) in '
            'User/Bugzilla.sublime-settings: ' + ', '.join(missing_keys))
        sublime.error_message(error)
        raise ValueError(error)

    return settings
