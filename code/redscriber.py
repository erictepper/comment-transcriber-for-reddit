import os
import praw.exceptions
import datetime
import snoomark


class RedditCommentTranscriber:
    LINE_LENGTH = 80

    def __init__(self):
        self._reddit = praw.Reddit('auth_info')  # auth information stored in git-ignored praw.ini file for
        # confidentiality

    def transcribe(self, start_comment_id, end_comment_id):
        start_comment = self._reddit.comment(id=start_comment_id)

        try:
            start_comment.refresh()  # obtains the CommentForest (i.e. list) of replies
            start_comment.replies.replace_more(limit=None)  # loads deeply-nested comments
        except praw.exceptions.ClientException:
            print('Start comment does not exist.')
            return

        # saves the file as date_[start_comment_id]_[end_comment_id].rtf
        file_name = str(datetime.datetime.utcnow().date()) + '_' + start_comment_id + '_' + end_comment_id + '.rtf'
        file_path = os.path.join('..', 'output', file_name)
        save_file = open(file_path, 'w')
        save_file.write('{')

        if end_comment_id == 'none' or start_comment_id == end_comment_id:
            self._print_single_comment(save_file, start_comment)
        elif end_comment_id == 'all':
            self._print_comment_tree(save_file, start_comment, 0)
        else:
            self._print_comment_chain(save_file, start_comment, end_comment_id, 0, list())

        save_file.write('}')
        save_file.close()

    def _print_single_comment(self, save_file, comment):  # todo: insert new line breaks when line overflows
        save_file.write('https://www.reddit.com' + comment.permalink + ' \\line \n')
        save_file.write('Transcribed ' + str(datetime.datetime.utcnow()) + ' \\line \n')
        save_file.write(' \\line \n')
        save_file.write(comment.author.name + '  ' + str(comment.score) + ' points  ' +
                        str(datetime.datetime.fromtimestamp(comment.created_utc)) + '  #' + comment.id + ' \\line \n')

        current_body = snoomark.comrak.to_html(self.string_cleaner(comment.body)).decode("utf-8")
        save_file.write(current_body)

        save_file.write(' \\line \n')

    def _print_comment_tree(self, save_file, root_comment, level):  # todo: insert new line breaks when line overflows
        if level == 0:
            save_file.write('https://www.reddit.com' + root_comment.permalink + ' \\line \n')
            save_file.write('Transcribed ' + str(datetime.datetime.utcnow()) + ' \\line \n')
            save_file.write(' \\line \n')

        indent_string = self._indent_level(level)

        try:
            save_file.write(indent_string + root_comment.author.name + '  ' + str(root_comment.score) + ' points  ' +
                            str(datetime.datetime.fromtimestamp(root_comment.created_utc)) + '  #' + root_comment.id +
                            ' \\line \n')
            comment_body_lines = self.string_cleaner(root_comment.body).splitlines()
            for line in comment_body_lines:
                for split_line in self.split_overflow(line):
                    save_file.write(indent_string + split_line + ' \\line \n')
        except AttributeError:
            save_file.write(indent_string + 'deleted/removed  #' + root_comment.id + ' \\line \n')
        save_file.write(indent_string + ' \\line \n')

        for reply in root_comment.replies:
            self._print_comment_tree(save_file, reply, level + 1)

    # Recursive depth-first search from the start comment to find the end comment
    # If end comment is found, adds the chain to the comment_stack and finally prints the comment_stack.
    # Returns True if end_comment is found in root_comment's descendants, False if it has not been found.
    def _print_comment_chain(self, save_file, root_comment, end_comment_id, level, comment_stack):  # todo: insert new line breaks when line overflows
        # Base case: root_comment is the end comment
        if root_comment.id == end_comment_id:
            comment_stack.append(root_comment)
            return True

        # Search through children to see if any of them are an ancestor of the end comment. If so, root_comment
        # is also an ancestor and therefore part of the chain, so add it to the comment stack
        found = False
        for reply in root_comment.replies:
            if self._print_comment_chain(save_file, reply, end_comment_id, level+1, comment_stack):
                comment_stack.append(root_comment)
                found = True
                if level != 0:
                    return found
                else:
                    break

        # If end comment is not found in root_comment's descendants, return False
        if not found:
            if level == 0:
                print('End comment was not found in thread.')
            return False

        # We will only reach this code if we are at the starting comment, the end-comment has been found, and
        # comment_stack contains the entire chain of comments with the starting comment on top and the ending
        # comment on bottom.
        # This code prints every comment on the comment_stack.
        while comment_stack:
            current = comment_stack.pop()
            if level == 0:
                save_file.write('https://www.reddit.com' + current.permalink + ' \\line \n')
                save_file.write('Transcribed ' + str(datetime.datetime.utcnow()) + ' \\line \n')
                save_file.write(' \\line \n')
            indent_string = self._indent_level(level)
            level += 1

            try:
                save_file.write(indent_string + current.author.name + '  ' + str(current.score) + ' points  ' +
                                str(datetime.datetime.fromtimestamp(current.created_utc)) + '  #' + current.id +
                                ' \\line \n')
                current_body = snoomark.comrak.to_html(self.string_cleaner(current.body)).decode("utf-8")
                comment_body_lines = current_body.splitlines()
                for line in comment_body_lines:
                    # for split_line in self.split_overflow(line):
                    #     save_file.write(indent_string + split_line + ' \\line \n')
                    save_file.write(indent_string + line + ' \\line \n')
            except AttributeError:
                save_file.write(indent_string + 'deleted/removed  #' + current.id + ' \\line \n')
            save_file.write(indent_string + ' \\line \n')

        return True

    @staticmethod
    def _indent_level(level):
        indent_string = ''

        for i in range(level):
            indent_string = indent_string + '| '

        return indent_string

    @staticmethod
    def string_cleaner(comment_text):
        comment_text = comment_text.replace('‘', '\'')
        return comment_text.replace('’', '\'')  # stub

    @classmethod
    def split_overflow(cls, line):
        words = line.split()
        return_lines = list()

        if line == '':
            return_lines.append('')
            return return_lines

        current_line = ''

        for word in words:
            if len(current_line) == 0 and len(word) > cls.LINE_LENGTH:
                return_lines.append(word)
            elif len(current_line + word) > cls.LINE_LENGTH:
                return_lines.append(current_line)
                current_line = word
            elif len(current_line) == 0:
                current_line = word
            else:
                current_line += ' ' + word

        if len(current_line) != 0:
            return_lines.append(current_line)

        return return_lines
