from multiprocessing import Process
# import unittest

from redscriber import RedditCommentTranscriber


if __name__ == '__main__':
    transcriber = RedditCommentTranscriber()

    # Non-existent start comment
    p1 = Process(target=transcriber.transcribe, args=('jfkdlszds', 'all',))
    p1.start()
    # transcriber.transcribe(start_comment_id='jfkdlszds', end_comment_id='all')
    p2 = Process(target=transcriber.transcribe, args=('jfkdlszds', 'none',))
    p2.start()
    # transcriber.transcribe(start_comment_id='jfkdlszds', end_comment_id='none')
    p3 = Process(target=transcriber.transcribe, args=('jfkdlszds', '1',))
    p3.start()
    # transcriber.transcribe(start_comment_id='jfkdlszds', end_comment_id='1')
    p4 = Process(target=transcriber.transcribe, args=('jfkdlszds', 'jkdsflajfkldsajlfsdka',))
    p4.start()
    # transcriber.transcribe(start_comment_id='jfkdlszds', end_comment_id='jkdsflajfkldsajlfsdka')

    # Single-comment transcription
    p5 = Process(target=transcriber.transcribe, args=('edfm15w', 'none',))
    p5.start()
    # transcriber.transcribe(start_comment_id='edfm15w', end_comment_id='none')
    p6 = Process(target=transcriber.transcribe, args=('edfme0h', 'none',))
    p6.start()
    # transcriber.transcribe(start_comment_id='edfme0h', end_comment_id='none')

    # Comment tree transcription
    p7 = Process(target=transcriber.transcribe, args=('eudig5e', 'all',))
    p7.start()
    # transcriber.transcribe(start_comment_id='eudig5e', end_comment_id='all')

    # Giant comment tree transcription
    p8 = Process(target=transcriber.transcribe, args=('edfm15w', 'all',))
    p8.start()
    # transcriber.transcribe(start_comment_id='edfm15w', end_comment_id='all')
    p9 = Process(target=transcriber.transcribe, args=('edge98h', 'none',))
    p9.start()
    # transcriber.transcribe(start_comment_id='edge98h', end_comment_id='none')  # - parser has problems with apostrophe

    # Comment chain transcription
    p10 = Process(target=transcriber.transcribe, args=('eqs3wsz', 'eqxjjs8',))
    p10.start()
    # transcriber.transcribe(start_comment_id='eqs3wsz', end_comment_id='eqxjjs8')
    p11 = Process(target=transcriber.transcribe, args=('edfm15w', 'edfme0h',))
    p11.start()
    # transcriber.transcribe(start_comment_id='edfm15w', end_comment_id='edfme0h')
    p12 = Process(target=transcriber.transcribe, args=('eulkvbp', 'eun0q9h',))
    p12.start()
    # transcriber.transcribe(start_comment_id='eulkvbp', end_comment_id='eun0q9h')

    # Emoji transcription
    # transcriber.transcribe(start_comment_id='dc2j4tb', end_comment_id='none')

    # Table markdown transcription
    p13 = Process(target=transcriber.transcribe, args=('ew6ld63', 'none',))
    p13.start()
    # transcriber.transcribe(start_comment_id='ew6ld63', end_comment_id='none')

    # Deleted account transcription
    p14 = Process(target=transcriber.transcribe, args=('dc2g3xq', 'none',))
    p14.start()
    # transcriber.transcribe(start_comment_id='dc2g3xq', end_comment_id='none')

    # Reddit user link & deleted account transcription
    p15 = Process(target=transcriber.transcribe, args=('dc20nhd', 'all',))
    p15.start()
    # transcriber.transcribe(start_comment_id='dc20nhd', end_comment_id='all')

    # Subreddit link transcription
    p7 = Process(target=transcriber.transcribe, args=('eow0ei7', 'none',))
    p7.start()
    # transcriber.transcribe(start_comment_id='eow0ei7', end_comment_id='none')

