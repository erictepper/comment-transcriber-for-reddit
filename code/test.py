# import unittest
from redscriber import RedditCommentTranscriber


if __name__ == '__main__':
    transcriber = RedditCommentTranscriber()

    # Comments for testing purposes:
    # Non-existent start comment
    transcriber.transcribe(start_comment_id='jfkdlszds', end_comment_id='all')
    transcriber.transcribe(start_comment_id='jfkdlszds', end_comment_id='none')
    transcriber.transcribe(start_comment_id='jfkdlszds', end_comment_id='1')
    transcriber.transcribe(start_comment_id='jfkdlszds', end_comment_id='jkdsflajfkldsajlfsdka')


    # Single-comment transcription
    transcriber.transcribe(start_comment_id='edfm15w', end_comment_id='none')

    # Comment tree transcription
    transcriber.transcribe(start_comment_id='eudig5e', end_comment_id='all')

    # Comment chain transcription
    transcriber.transcribe(start_comment_id='eqs3wsz', end_comment_id='eqxjjs8')