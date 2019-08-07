# Reddit Comment Transcriber
A program that converts a thread of Reddit comments to a rich text file (.rtf). 

The following files contain code written exclusively by me:
- main.py
- redscriber.py
- test.py
- working_regex.txt

The following files contain code written by others with modifications by me<sup>1</sup>:
- code/comrak/src/html.rs<sup>2</sup>
- code/pulldown-cmark/src/main.rs<sup>3</sup>

output/ contains the output .rtf files of the test cases I have written. 

#### To-do
1. Fix bug where program fails where user has been deleted, but comment still exists.
2. Create function that handles unordered/ordered list html parsing.
3. Add support for emojis. 
4. Add support for username links (i.e. /u/username)

#### Credits

- code/snoomark.py - https://github.com/zeantsoi/snoomark-binding
- code/comrak/ - https://github.com/zeantsoi/comrak
- code/pulldown-cmark/ - https://github.com/zeantsoi/pulldown-cmark

From what I can tell, these cited projects are officially used for parsing 
Reddit's markdown and converting it to html. They are required in my project in order to take the text formatting that 
Reddit uses (SnooMark) and convert it into .rtf formatting. code/comrak is the program that I am using for parsing the 
markdown as I ran into errors using pulldown-cmark. 

---

1. Modifications are marked with the comment 'edited by erictepper'
2. Changed the output of the parser from .html syntax to .rtf syntax
3. Added a main() function so the project would build. 