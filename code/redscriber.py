import os
import datetime
import time
import re

import praw.exceptions
from gitmark import CMarkGFM


class RedditCommentTranscriber:

    def __init__(self):
        self._reddit = praw.Reddit('auth_info')  # auth information stored in git-ignored praw.ini file for
        # confidentiality
        self._indent = 0  # keeps track of the most recent indent-level for use in list transcription

    def transcribe(self, start_comment_id, end_comment_id):
        start = time.time()
        if end_comment_id != 'all' and end_comment_id != 'none':
            start_comment = self._reddit.comment(id=end_comment_id)
            using_start_comment = False
        else:
            start_comment = self._reddit.comment(id=start_comment_id)
            using_start_comment = True

        try:
            start_comment.refresh()  # obtains the CommentForest (i.e. list) of replies
        except praw.exceptions.ClientException:
            if using_start_comment:
                print('Start comment does not exist.')
            else:
                print('End comment does not exist.')
            return

        if end_comment_id == 'all':
            start_comment.replies.replace_more(limit=None)  # loads deeply-nested comments
        end = time.time()
        print('Accessing Reddit took %f seconds for comments %s, %s.' % (end-start, start_comment_id, end_comment_id))

        start = time.time()
        # saves the file as date_[start_comment_id]_[end_comment_id].rtf
        file_name = str(datetime.datetime.utcnow().date()) + '_' + start_comment_id + '_' + end_comment_id + '.rtf'
        file_path = os.path.join('..', 'output', file_name)
        save_file = open(file_path, 'w')
        save_file.write(r'{\rtf1\ansi\ansicpg1252' + '\n')

        # colortbl is tied to the blockquote parsing in comrak/src/html.rs,
        # which uses the 2nd entry in the colortbl (0-indexed)
        save_file.write(r'{\colortbl;\red255\green255\blue255;\red0\green0\blue0;\red85\green142\blue40;' +
                        r'\red127\green127\blue127;}' + '\n' +
                        r'{\*\expandedcolortbl;;\cssrgb\c39975\c61335\c20601;\cssrgb\c57046\c57047\c57046;}' + '\n')

        #if start_comment_id == 'edfm15w' or start_comment_id == 'edfme0h' or start_comment_id == 'ew6ld63':  # todo: testing
        #    file_path_2 = os.path.join('..', 'output', start_comment_id + '_superscript_comment.txt')  # todo: testing
        #    save_file_2 = open(file_path_2, 'w')  # todo: testing
        #    save_file_2.write(re.sub(r'(\^)((?:\^*)(?:(?:{\\field{\\\*\\fldinst{HYPERLINK ".+?"}}{\\fldrslt .+?}})|(?:\(.+?\))|(?:.+?)))(?= |\n|\*|$|\\)',
        #                             self._format_superscript, start_comment.body))  # todo: testing
        #    save_file_2.write(CMarkGFM.md2html(start_comment.body))
        #    save_file_2.close()  # todo: testing

        if end_comment_id == 'none' or start_comment_id == end_comment_id:
            self._write_single_comment(save_file, start_comment)
        elif end_comment_id == 'all':
            self._write_comment_tree(save_file, start_comment, 0)
        else:
            try:
                # self._write_comment_chain(save_file, start_comment, end_comment_id, 0, list())
                self._write_comment_chain_up(save_file, list(), start_comment, start_comment_id)
            except praw.exceptions.ClientException as e:
                print(str(e))
                save_file.close()
                os.remove(file_path)
                return

        save_file.write('}')
        save_file.close()
        end = time.time()
        print('Writing to the file took %f seconds for comments %s, %s.' %
              (end-start, start_comment_id, end_comment_id))

    def _write_single_comment(self, save_file, comment):
        submission_link = 'https://www.reddit.com' + comment.submission.permalink
        self._write_comment(save_file=save_file, comment=comment, submission_link=submission_link, level=0)

    def _write_comment_tree(self, save_file, root_comment, level):
        submission_link = 'https://www.reddit.com' + root_comment.submission.permalink
        self._write_comment(save_file=save_file, comment=root_comment, submission_link=submission_link, level=level)

        # Recursively write the comment replies
        for reply in root_comment.replies:
            self._write_comment_tree(save_file, reply, level + 1)

    # ----DEPRECATED----
    # Recursive depth-first search from the start comment to find the end comment
    # If end comment is found, adds the chain to the comment_stack and finally prints the comment_stack.
    # Returns True if end_comment is found in root_comment's descendants, False if it has not been found.
    def _write_comment_chain(self, save_file, root_comment, end_comment_id, level, comment_stack):
        # Base case: root_comment is the end comment
        if root_comment.id == end_comment_id:
            comment_stack.append(root_comment)
            return True

        # Search through children to see if any of them are an ancestor of the end comment. If so, root_comment
        # is also an ancestor and therefore part of the chain, so add it to the comment stack
        found = False
        for reply in root_comment.replies:
            if self._write_comment_chain(save_file, reply, end_comment_id, level + 1, comment_stack):
                comment_stack.append(root_comment)
                found = True
                if level != 0:
                    return found
                else:
                    break

        # If end comment is not found in root_comment's descendants, return False
        if not found:
            if level == 0:
                raise praw.exceptions.ClientException('End comment was not found in thread.')
            return False

        # We will only reach this code if we are at the starting comment, the end-comment has been found, and
        # comment_stack contains the entire chain of comments with the starting comment on top and the ending
        # comment on bottom.
        # This code writes every comment on the comment_stack to the save file.
        submission_link = 'https://www.reddit.com' + root_comment.submission.permalink
        while comment_stack:
            current = comment_stack.pop()
            self._write_comment(save_file=save_file, comment=current, submission_link=submission_link, level=level)
            level += 1

        return True

    def _write_comment_chain_up(self, save_file, comment_stack, comment, ancestor_id):
        refresh_counter = 0

        # Searches upwards from the descendant comment to try to find the ancestor comment
        while comment.id != ancestor_id:
            if comment.is_root:
                raise praw.exceptions.ClientException('Start comment and end comment were not found within the same '
                                                      'thread.')
            if refresh_counter % 9 == 0:
                comment.refresh()
            refresh_counter += 1
            comment_stack.append(comment)
            comment = comment.parent()

        # Appends the first comment in the chain to the stack. 
        comment_stack.append(comment)

        submission_link = 'https://www.reddit.com' + comment.submission.permalink
        level = 0
        while comment_stack:
            current = comment_stack.pop()
            self._write_comment(save_file=save_file, comment=current, submission_link=submission_link, level=level)
            level += 1

    def _write_comment(self, save_file, comment, submission_link, level):
        comment_permalink = submission_link + comment.id + '/'

        # Write the file header
        if level == 0:
            save_file.write(r'\pard {\field{\*\fldinst{HYPERLINK "' + comment_permalink)
            save_file.write(r'"}}{\fldrslt ' + comment_permalink + '}}\\\n')
            save_file.write('Transcribed ' + datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S') + '\\\n')
            save_file.write('\\\n')

        indent_string = self._indent_level(level)

        # Write the comment info line
        # author link
        try:
            comment_author_header = r'{\field{\*\fldinst{HYPERLINK "https://www.reddit.com/user/'
            comment_author_header += comment.author.name + r'/"}}{\fldrslt ' + comment.author.name + '}}'
        except AttributeError:
            comment_author_header = '[deleted]'
        # comment permalink
        comment_permalink_header = r'{\field{\*\fldinst{HYPERLINK "' + comment_permalink
        comment_permalink_header += r'"}}{\fldrslt #' + comment.id + '}}'
        # write info line
        save_file.write(indent_string + '\\fs22 \\cf3 ' + comment_author_header + '  ' + str(comment.score) +
                        ' points  ' + str(datetime.datetime.fromtimestamp(comment.created_utc)) + '  ' +
                        comment_permalink_header + '\\fs24 \\cf0 \\\n')

        # Write the comment body
        comment_body = self.string_cleaner(CMarkGFM.md2html(comment.body))
        current_body = re.sub(r'(\^)((?:\^*)'
                              r'(?:(?:{\\field{\\\*\\fldinst{HYPERLINK ".+?"}}{\\fldrslt .+?}})|(?:\(.+?\))|(?:.+?)))'
                              r'(?= |\n|\*|$|\\)',
                              self._format_superscript, comment_body)
        current_body = re.sub(r'<((?:ol)|(?:ul))((?: start=.+?)?)>((?:.|\n|\r)+?)</\1>', self._format_lists,
                              current_body)
        save_file.write(current_body)

    def _indent_level(self, level):
        self._indent = level
        indent_string = '\\pard\\li' + str(140*level) + '\\fi0\\pardirnatural\\partightenfactor0\n'

        return indent_string

    @staticmethod
    def string_cleaner(comment_text):
        comment_text = comment_text.replace('—', r'\'97')
        comment_text = comment_text.replace('’', r'\'92')
        comment_text = comment_text.replace(' ', ' ')
        comment_text = comment_text.replace(r'&quot;', '"')
        comment_text = comment_text.replace('“', r'\'93')
        comment_text = comment_text.replace('”', r'\'94')
        comment_text = comment_text.replace('&amp;', '&')
        return comment_text.replace('‘', r'\'91')

    @classmethod
    def _format_superscript(cls, match):
        group2 = re.sub(r'(\^)((?:\^*)'
                        r'(?:(?:{\\field{\\\*\\fldinst{HYPERLINK ".+?"}}{\\fldrslt .+?}})|(?:\(.+?\))|(?:.+?)))'
                        r'(?= |\n|\*|$|\\)',
                        cls._format_superscript, match.group(2))

        return r'\super \fs18 ' + group2 + r'\nosupersub \fs24 '

    def _format_lists(self, match):
        indent_string = self._list_indent_level()
        previous_indent_string = self._indent_level(self._indent)
        tag = match.group(1)
        try:
            starting_number = re.search(r'[0-9]+', match.group(2)).group(0)
        except AttributeError:
            starting_number = None
        if tag == 'ol':
            if starting_number:
                parser = OrderedListParser(int(starting_number))
            else:
                parser = OrderedListParser()

            return indent_string + \
                   re.sub(r'<(li)>((?:.|\n|\r)+?)</\1>', parser.format_ordered_list_items, match.group(3)) + \
                   previous_indent_string
        else:
            return indent_string + \
                   re.sub(r'<(li)>((?:.|\n|\r)+?)</\1>', self._format_unordered_list_items, match.group(3)) + \
                   previous_indent_string

    def _list_indent_level(self):
        list_tab = 140 * (self._indent + 1)
        text_tab = 140 * (self._indent + 4)
        indent_string = '\\pard\\tx' + str(list_tab) + '\\tx' + str(text_tab) + '\\li' + str(text_tab) + '\\fi-' + \
                        str(text_tab) + '\\pardirnatural\\partightenfactor0\n'

        return indent_string

    @staticmethod
    def _format_unordered_list_items(match):
        list_text = match.group(2)
        end = len(list_text)
        if end >= 4 and list_text[end-4:end] == '\\\n\\\n':
            append = ''
        else:
            append = '\\\n\\\n'
        return '{\\listtext\t\\uc0\\u8226\t}' + list_text + append


class OrderedListParser:

    def __init__(self, start=1):
        self.item_number = start

    def format_ordered_list_items(self, match):
        list_text = match.group(2)

        if len(list_text) >= 4 and list_text[len(list_text)-4:len(list_text)] == '\\\n\\\n':
            end = ''
        else:
            end = '\\\n\\\n'

        return_string = '{\\listtext\t' + str(self.item_number) + '.\t}' + list_text + end

        self.item_number += 1

        return return_string
