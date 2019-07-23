import sys
import praw


def print_single_comment(comment):
    return  # stub


def print_comment_tree(root_comment):
    return  # stub


def print_comment_chain(root_comment, end_comment_id):
    return  # stub


if __name__ == '__main__':
    reddit = praw.Reddit('auth_info')  # information stored in gitignored praw.ini file for confidentiality

    start_comment_id = input('ID of start comment: ')
    end_comment_id = input('ID of end comment (or \'all\' to print all children, or \'none\' to print no children): ')

    start_comment = reddit.comment(id=start_comment_id)  # non-existent comment for testing: jfkdlszds

    try:
        start_comment.body
    except praw.exceptions.ClientException:
        print('Start comment does not exist.')
        sys.exit()

    if end_comment_id == 'none':
        print_single_comment(start_comment)
    elif end_comment_id == 'all':
        print_comment_tree(start_comment)
    else:
        print_comment_chain(start_comment, end_comment_id)
