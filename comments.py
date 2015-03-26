import sublime, sublime_plugin

from .utils import bugzilla_command

class BugzillaViewCommentsCommand(sublime_plugin.WindowCommand):
    def run(self, **kwargs):
        bug_id = kwargs['bug_id']
        comments = bugzilla_command('comment', bug_id)

        view = self.window.new_file()
        view.set_scratch(True)
        view.set_name('View Comments: Bug ' + bug_id)
        view.run_command("bugzilla_inject_text", {'text': comments})
        view.sel().clear()
        view.sel().add(sublime.Region(0,0))



class BugzillaNewCommentCommand(sublime_plugin.WindowCommand):

    active_comment = None

    def run(self, **kwargs):
        if BugzillaNewCommentCommand.active_comment:
            print('Cannot start new comment -- '
                'a comment buffer is already active.')
        BugzillaNewCommentCommand.active_comment = self

        self.bug_id = kwargs['bug_id']
        comments = bugzilla_command('comment', self.bug_id)
        page_text = '\n\n' + COMMENT_SEPARATOR + comments

        self.comment_view = self.window.new_file()
        self.comment_view.set_scratch(True)
        self.comment_view.set_name('New Comment: Bug ' + self.bug_id)
        self.comment_view.run_command(
            "bugzilla_inject_text", {'text': page_text})
        self.comment_view.sel().clear()
        self.comment_view.sel().add(sublime.Region(0,0))


    def submit(self):
        buffer_split = self.comment_view.substr(
            sublime.Region(
                0,
                self.comment_view.size())
            ).split(COMMENT_SEPARATOR)

        if len(buffer_split) < 2:
            print('Invalid comment buffer -- comment separator not found.')
            print('No comment will be submitted.')
            return

        comment_text = buffer_split[0].strip()

        if not comment_text:
            print('Comment is empty, and will not be submitted.')
            return

        bugzilla_command('comment', self.bug_id, '--message', comment_text)

        BugzillaNewCommentCommand.active_comment = None


class BugzillaCommentViewListener(sublime_plugin.EventListener):
    def on_close(self, view):
        active_comment = BugzillaNewCommentCommand.active_comment

        if active_comment and view == active_comment.comment_view:
            active_comment.submit()


COMMENT_SEPARATOR = '''
===========================================================================
Write reply above, then close window to submit.

If the area above is empty (or contains only whitespace), no comment will
be submitted.
===========================================================================
'''
