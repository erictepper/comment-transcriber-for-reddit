# Transcriber for Reddit Comments
### General Info
Version 0.9.1

A program that converts a thread of Reddit comments to a rich text file (.rtf). 

The following files contain code written exclusively by me:
- main.py
- redscriber.py
- test.py
- working_regex.txt

The following files contain code written by others with modifications by me<sup>1</sup>:
- code/cmark-gfm/src/html.c<sup>2</sup>

output/ contains the output .rtf files of the test cases I have written. (Not currently included in the repo)

### Versions
**Version 0.1:** Basic transcriber that writes to plain .txt files; able to write a single comment.

**Version 0.2:** Implemented method and functionality to write an entire tree of comments (the beginning comment plus 
all of its descendants).

**Version 0.3:** Implemented method and functionality to write a single thread of comments, starting with the beginning 
comment and ending with *one* of its descendants, and the chain of comments between the start and end comment. 


**Version 0.4:** Modified transcriber to write in the .rtf file format, rather than .txt, creating the potential for 
richer, easier-to-read text formatting. 

**Version 0.5:** Implemented and modified Reddit's markdown parser, 
[snoomark-binding](https://github.com/zeantsoi/snoomark-binding), to convert markdown (a form of plain text formatting) 
in comments to .rtf formatting, substantially increasing readability of comments.

**Version 0.6:** Implemented and modified a new Markdown parser, GitHub's 
[cmark-gfm](https://github.com/github/cmark-gfm) (an upstream version of Reddit's Markdown parser), due to bugs in 
the previous parser. 

**Version 0.7:** Implemented functionality using regular expressions to parse Markdown superscript and convert it into 
.rtf formatting (as GitHub's parser does not implement functionality for superscript). Superscript will now be properly 
displayed in result .rtf files. 

**Version 0.8:** Implemented functionality using regular expressions to parse the HTML output of the parser for lists 
(ol, ul, and li elements) and convert it to .rtf list syntax. Lists will now be properly displayed in result .rtf 
files. 

**Version 0.9:** Changed _write_comment_chain from a depth-first-search implementation to a bottom-up linear search 
implementation, for a potential speed increase. 
* **0.9.1:** Test cases now use multiprocessing to run. 

### To-do
###### Features to Add
1. Use parser's table, strikethrough, and autolink extensions. 
2. Add support for emojis. 
3. Remove testing code from redscriber.py.
4. Write privacy policy. 
5. Add transcription for submissions.
    1. Transcription of all comments.
    2. Transcription of a single comment.
    3. Transcription of a comment chain. 

###### Bugs to Fix
- No currently known bugs.

### Credits

- code/cmark-gfm - https://github.com/github/cmark-gfm

From what I can tell, the above cited project is an upstream version of the program used for parsing 
Reddit's markdown and converting it to html. It is required in my project in order to take the text formatting that 
Reddit uses (SnooMark) and convert it into .rtf formatting. I have had to do superscript parsing myself, and then also 
parse the html output for ordered/unordered lists in order to convert it to .rtf formatting. 

---

1. Modifications are marked with the comment 'edited by erictepper'
2. Changed the output of the parser from .html syntax to .rtf syntax