import sys
import praw.exceptions
import datetime


def print_single_comment(comment):
    print('https://www.reddit.com' + comment.permalink)
    print()
    print(comment.author.name + ' ', str(comment.score), 'points ',
          datetime.datetime.fromtimestamp(comment.created_utc))
    print(comment.body)
    print()


def print_comment_tree(root_comment, level):
    if level == 0:
        print('https://www.reddit.com' + root_comment.permalink)
        print()

    indent_string = indent_level(level)

    print(indent_string + root_comment.author.name + ' ', str(root_comment.score), 'points ',
          datetime.datetime.fromtimestamp(root_comment.created_utc))
    print(indent_string + root_comment.body)
    print(indent_string)

    root_comment.refresh()
    for reply in root_comment.replies:
        print_comment_tree(reply, level+1)


def print_comment_chain(root_comment, end_comment_id, level):
    return  # stub


def indent_level(level):
    indent_string = ''

    for i in range(level):
        indent_string = indent_string + '| '

    return indent_string


if __name__ == '__main__':
    # Comments for testing purposes:
    # Non-existent: jfkdlszds
    # PoppinKream: edfm15w
    # Korok seeds: eudig5e

    reddit = praw.Reddit('auth_info')  # auth information stored in git-ignored praw.ini file for confidentiality

    start_comment_id = input('ID of start comment: ')
    end_comment_id = input('ID of end comment (or \'all\' to print all children, or \'none\' to print no children): ')

    start_comment = reddit.comment(id=start_comment_id)

    try:
        start_comment.body
    except praw.exceptions.ClientException:
        print('Start comment does not exist.')
        sys.exit()

    if end_comment_id == 'none' or start_comment_id == end_comment_id:
        print_single_comment(start_comment)
    elif end_comment_id == 'all':
        print_comment_tree(start_comment, 0)
    else:
        print_comment_chain(start_comment, end_comment_id, 0)
