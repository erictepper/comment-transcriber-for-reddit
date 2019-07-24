import praw.exceptions
import datetime


class RedditCommentTranscriber:

    def __init__(self):
        self.reddit = praw.Reddit('auth_info')  # auth information stored in git-ignored praw.ini file for
        # confidentiality

    def transcribe(self, start_comment_id, end_comment_id):
        start_comment = self.reddit.comment(id=start_comment_id)

        try:
            start_comment.body  # a check to make sure the start comment exists
        except praw.exceptions.ClientException:
            print('Start comment does not exist.')
            return

        if end_comment_id == 'none' or start_comment_id == end_comment_id:
            self._print_single_comment(start_comment)
        elif end_comment_id == 'all':
            self._print_comment_tree(start_comment, 0)
        else:
            self._print_comment_chain(start_comment, end_comment_id, 0, list())

    @staticmethod
    def _indent_level(level):
        indent_string = ''

        for i in range(level):
            indent_string = indent_string + '| '

        return indent_string

    @staticmethod
    def _print_single_comment(comment):
        print('https://www.reddit.com' + comment.permalink)
        print()
        print(comment.author.name + ' ', str(comment.score), 'points ',
              datetime.datetime.fromtimestamp(comment.created_utc))
        print(comment.body)
        print()

    def _print_comment_tree(self, root_comment, level):  # todo: insert new line breaks when line overflows
        if level == 0:
            print('https://www.reddit.com' + root_comment.permalink)
            print()

        indent_string = self._indent_level(level)

        try:
            print(indent_string + root_comment.author.name + ' ', str(root_comment.score), 'points ',
                  datetime.datetime.fromtimestamp(root_comment.created_utc))
            comment_body_lines = root_comment.body.splitlines()
            for line in comment_body_lines:
                print(indent_string + line)
        except AttributeError:
            print(indent_string + 'deleted/removed')
        print(indent_string)

        root_comment.refresh()
        for reply in root_comment.replies:
            self._print_comment_tree(reply, level + 1)

    def _print_comment_chain(self, root_comment, end_comment_id, level, comment_stack):
        if root_comment.id == end_comment_id:
            comment_stack.append(root_comment)
            return True

        root_comment.refresh()

        found = False
        for reply in root_comment.replies:
            if self._print_comment_chain(reply, end_comment_id, level+1, comment_stack):
                comment_stack.append(root_comment)
                found = True
                if level != 0:
                    return found
                else:
                    break

        if not found:
            if level == 0:
                print('End comment was not found in thread.')
            return False

        while comment_stack:
            current = comment_stack.pop()
            if level == 0:
                print('https://www.reddit.com' + root_comment.permalink)
                print()
            indent_string = self._indent_level(level)
            level += 1

            try:
                print(indent_string + current.author.name + ' ', str(current.score), 'points ',
                      datetime.datetime.fromtimestamp(current.created_utc))
                comment_body_lines = current.body.splitlines()
                for line in comment_body_lines:
                    print(indent_string + line)
            except AttributeError:
                print(indent_string + 'deleted/removed')
            print(indent_string)

        return True
