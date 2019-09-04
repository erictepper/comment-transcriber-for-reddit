import time

from redscriber import RedditCommentTranscriber


if __name__ == '__main__':

    start_comment_id = input('ID of start comment: ')
    end_comment_id = input('ID of end comment (or \'all\' to print all children, or \'none\' to print no children): ')

    start = time.time()
    transcriber = RedditCommentTranscriber()
    transcriber.transcribe(start_comment_id=start_comment_id, end_comment_id=end_comment_id)
    end = time.time()
    print('Transcribed comment thread in %f s.' % (end-start))
