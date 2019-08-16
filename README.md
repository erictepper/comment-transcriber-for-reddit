# Comment Transcriber for Reddit
A program that converts a thread of Reddit comments to a rich text file (.rtf). 

The following files contain code written exclusively by me:
- main.py
- redscriber.py
- test.py
- working_regex.txt

The following files contain code written by others with modifications by me<sup>1</sup>:
- code/cmark-gfm/src/html.c<sup>2</sup>

output/ contains the output .rtf files of the test cases I have written. (Not currently included in the repo)

#### To-do
1. Use parser's table, strikethrough, and autolink extensions. 
2. Add support for emojis. 
3. Change _write_comment_chain from DFS implementation to bottom-up transcription for potential speed increase.
4. Remove testing code from redscriber.py.
5. Write version info.
6. Write privacy policy. 
7. Add transcription for submissions.
    1. Transcription of all comments.
    2. Transcription of a single comment.
    3. Transcription of a comment chain. 

#### Credits

- code/cmark-gfm - https://github.com/github/cmark-gfm

From what I can tell, the above cited project is an upstream version of the program used for parsing 
Reddit's markdown and converting it to html. It is required in my project in order to take the text formatting that 
Reddit uses (SnooMark) and convert it into .rtf formatting. I have had to do superscript parsing myself, and then also 
parse the html output for ordered/unordered lists in order to convert it to .rtf formatting. 

---

1. Modifications are marked with the comment 'edited by erictepper'
2. Changed the output of the parser from .html syntax to .rtf syntax