from redscriber import RedditCommentTranscriber


if __name__ == '__main__':
    # Comments for testing purposes:
    # Non-existent: jfkdlszds
    # PoppinKream: edfm15w
    # Korok seeds: eudig5e

    start_comment_id = input('ID of start comment: ')
    end_comment_id = input('ID of end comment (or \'all\' to print all children, or \'none\' to print no children): ')

    transcriber = RedditCommentTranscriber()
    transcriber.transcribe(start_comment_id=start_comment_id, end_comment_id=end_comment_id)
