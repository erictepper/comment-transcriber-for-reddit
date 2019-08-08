# Reddit Comment Transcriber
A program that converts a thread of Reddit comments to a rich text file (.rtf). 

The following files contain code written exclusively by me:
- main.py
- redscriber.py
- test.py
- working_regex.txt

The following files contain code written by others with modifications by me<sup>1</sup>:
- code/comrak/src/html.rs<sup>2</sup>
- code/comrak/src/lib.rs<sup>3</sup>
- code/pulldown-cmark/src/main.rs<sup>4</sup>
- code/comrak/src/parser/autolink.rs<sup>5</sup>

output/ contains the output .rtf files of the test cases I have written. 

#### To-do
1. Create function that handles unordered/ordered list html parsing.
2. Add support for emojis. 

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
3. Added comments for debugging.
4. Added an empty main() function so the project would build. <!---Not included in the repository, as the changes were unsubstantial and therefore not worth including in my repository.--->
5. Modified code to support the parsing of Reddit-specific links. 