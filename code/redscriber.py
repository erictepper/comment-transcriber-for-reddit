import os
import datetime
import re

import praw.exceptions
# import snoomark
from gitmark import CMarkGFM


class RedditCommentTranscriber:
    LINE_LENGTH = 80

    def __init__(self):
        self._reddit = praw.Reddit('auth_info')  # auth information stored in git-ignored praw.ini file for
        self._indent = 0  # keeps track of the most recent indent-level for use in list transcription
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
        save_file.write(r'{\rtf1\ansi\ansicpg1252' + '\n')

        # colortbl is tied to the blockquote parsing in comrak/src/html.rs,
        # which uses the 2nd entry in the colortbl (0-indexed)
        save_file.write(r'{\colortbl;\red255\green255\blue255;\red0\green0\blue0;\red85\green142\blue40;' +
                        r'\red127\green127\blue127;}' + '\n' +
                        r'{\*\expandedcolortbl;;\cssrgb\c39975\c61335\c20601;\cssrgb\c57046\c57047\c57046;}' + '\n')

        # if start_comment_id == 'edfm15w' or start_comment_id == 'edfme0h' or start_comment_id == 'ew6ld63':  # todo: testing
        #     file_path_2 = os.path.join('..', 'output', start_comment_id + '_superscript_comment.txt')  # todo: testing
        #     save_file_2 = open(file_path_2, 'w')  # todo: testing
        #     #save_file_2.write(re.sub(r'(\^)((?:\^*)(?:(?:{\\field{\\\*\\fldinst{HYPERLINK ".+?"}}{\\fldrslt .+?}})|(?:\(.+?\))|(?:.+?)))(?= |\n|\*|$|\\)',
        #     #                         self._format_superscript_for_parser, start_comment.body))  # todo: testing
        #     save_file_2.write(CMarkGFM.md2html(start_comment.body))
        #     save_file_2.close()  # todo: testing

        if end_comment_id == 'none' or start_comment_id == end_comment_id:
            self._write_single_comment(save_file, start_comment)
        elif end_comment_id == 'all':
            self._write_comment_tree(save_file, start_comment, 0)
        else:
            self._write_comment_chain(save_file, start_comment, end_comment_id, 0, list())

        save_file.write('}')
        save_file.close()

    def _write_single_comment(self, save_file, comment):
        submission_link = 'https://www.reddit.com' + comment.submission.permalink
        self._write_comment(save_file=save_file, comment=comment, submission_link=submission_link, level=0)

    def _write_comment_tree(self, save_file, root_comment, level):
        submission_link = 'https://www.reddit.com' + root_comment.submission.permalink
        self._write_comment(save_file=save_file, comment=root_comment, submission_link=submission_link, level=level)

        # Recursively write the comment replies
        for reply in root_comment.replies:
            self._write_comment_tree(save_file, reply, level + 1)

    # Recursive depth-first search from the start comment to find the end comment
    # If end comment is found, adds the chain to the comment_stack and finally prints the comment_stack.
    # Returns True if end_comment is found in root_comment's descendants, False if it has not been found.
    def _write_comment_chain(self, save_file, root_comment, end_comment_id, level, comment_stack):  # todo: change from DFS implementation to bottom-up transcription for speed
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
                print('End comment was not found in thread.')  # todo: raise praw.exceptions.ClientException if end comment not found
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
                              self._format_superscript_for_parser, comment_body)
        current_body = re.sub(r'<((?:ol)|(?:ul))((?: start=.+?)?)>((?:.|\n|\r)+?)</\1>', self._format_lists_for_parser,
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
    def _format_superscript_for_parser(cls, text):
        group2 = re.sub(r'(\^)((?:\^*)'
                        r'(?:(?:{\\field{\\\*\\fldinst{HYPERLINK ".+?"}}{\\fldrslt .+?}})|(?:\(.+?\))|(?:.+?)))'
                        r'(?= |\n|\*|$|\\)',
                        cls._format_superscript_for_parser, text.group(2))

        return r'\super \fs18 ' + group2 + r'\nosupersub \fs24 '

    def _format_lists_for_parser(self, regex):
        indent_string = self._list_indent_level()
        previous_indent_string = self._indent_level(self._indent)
        tag = regex.group(1)
        try:
            starting_number = re.search(r'[0-9]+', regex.group(2)).group(0)
        except AttributeError:
            starting_number = None
        if tag == 'ol':
            if starting_number:
                parser = OrderedListParser(int(starting_number))
            else:
                parser = OrderedListParser()

            return indent_string + \
                re.sub(r'<(li)>((?:.|\n|\r)+?)</\1>', parser.format_ordered_list_items, regex.group(3)) + \
                previous_indent_string
        else:
            return indent_string + \
                   re.sub(r'<(li)>((?:.|\n|\r)+?)</\1>', self._format_unordered_list_items, regex.group(3)) + \
                   previous_indent_string

    def _list_indent_level(self):
        list_tab = 140 * (self._indent + 1)
        text_tab = 140 * (self._indent + 4)
        indent_string = '\\pard\\tx' + str(list_tab) + '\\tx' + str(text_tab) + '\\li' + str(text_tab) + '\\fi-' + \
                        str(text_tab) + '\\pardirnatural\\partightenfactor0\n'

        return indent_string

    @classmethod
    def _format_unordered_list_items(cls, text):
        my_text = text.group(2)
        if len(my_text) >= 4 and my_text[len(my_text)-4:len(my_text)] == '\\\n\\\n':
            end = ''
        else:
            end = '\\\n\\\n'
        return '{\\listtext\t\\uc0\\u8226\t}' + text.group(2) + end

    # Not currently in use
    @staticmethod
    def string_pre_cleaner(comment_text):
        comment_text = comment_text.replace('—', r"\\'97")
        comment_text = comment_text.replace('’', r"\\'92")
        comment_text = comment_text.replace('“', r"\\'93")
        comment_text = comment_text.replace('”', r"\\'94")
        return comment_text.replace('‘', r"\\'91")


class OrderedListParser:

    def __init__(self, start=1):
        self.item_number = start

    def format_ordered_list_items(self, text):
        my_text = text.group(2)
        if len(my_text) >= 4 and my_text[len(my_text)-4:len(my_text)] == '\\\n\\\n':
            end = ''
        else:
            end = '\\\n\\\n'
        return_string = '{\\listtext\t' + str(self.item_number) + '.\t}' + text.group(2) + end
        self.item_number += 1
        return return_string
