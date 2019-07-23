import praw


if __name__ == '__main__':
    reddit = praw.Reddit('authInfo')  # information stored in gitignored praw.ini file for confidentiality

    start_comment_id = input("ID of start comment: ")
    end_comment_id = input("ID of end comment: ")

    
