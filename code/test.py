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
    transcriber.transcribe(start_comment_id='edfme0h', end_comment_id='none')

    # Comment tree transcription
    transcriber.transcribe(start_comment_id='eudig5e', end_comment_id='all')

    # Giant comment tree transcription
    transcriber.transcribe(start_comment_id='edfm15w', end_comment_id='all')
    # transcriber.transcribe(start_comment_id='edge98h', end_comment_id='none') - parser has problems with apostrophe

    # Comment chain transcription
    transcriber.transcribe(start_comment_id='eqs3wsz', end_comment_id='eqxjjs8')
    transcriber.transcribe(start_comment_id='edfm15w', end_comment_id='edfme0h')
    transcriber.transcribe(start_comment_id='eulkvbp', end_comment_id='eun0q9h')

    # Emoji transcription
    # transcriber.transcribe(start_comment_id='dc2j4tb', end_comment_id='none')

    # Table markdown transcription
    # transcriber.transcribe(start_comment_id='ew6ld63', end_comment_id='none')

    # Deleted account transcription
    # transcriber.transcribe(start_comment_id='dc2g3xq', end_comment_id='none')

