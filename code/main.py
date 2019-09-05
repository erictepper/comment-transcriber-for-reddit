from redscriber import RedditCommentTranscriber


if __name__ == '__main__':

    start_comment_id = input('ID of start comment: ')
    end_comment_id = input('ID of end comment (or \'all\' to print all children, or \'none\' to print no children): ')

    transcriber = RedditCommentTranscriber()
    transcriber.transcribe(start_comment_id=start_comment_id, end_comment_id=end_comment_id)
    print('Transcribed comment thread in %f s.' % (end-start))
