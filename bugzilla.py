import sublime_plugin

from .utils import bugzilla_command

class BugzillaTitleCommand(sublime_plugin.TextCommand):
    '''Outputs the title of the given bug to the current buffer.'''
    def run(self, edit, **kwargs):
        bug_id = kwargs['bug_id']
        title = bugzilla_command('list', bug_id)

        self.view.run_command("bugzilla_inject_text", {'text': title})
