# Reddit Comment Transcriber
A program that converts a thread of Reddit comments to a rich text file. 

The following files contain code written exclusively by me:
- main.py
- redscriber.py
- test.py
- working_regex.txt

The following files contain code written by others with modifications by me<sup>1</sup>:
- code/comrak/src/html.rs

output/ contains the output .rtf files of the test cases I have written. 

#### Credits

- code/snoomark.py - https://github.com/zeantsoi/snoomark-binding
- code/comrak/ - https://github.com/zeantsoi/comrak
- code/pulldown-cmark/ - https://github.com/zeantsoi/pulldown-cmark

From what I can tell, these cited projects are officially used for parsing 
Reddit's markdown and converting it to html. They are required in my project in order to take the text formatting that 
Reddit uses and convert it into .rtf formatting. code/comrak/src/html.rs has been edited by me to change the output of 
the parser from html tags to .rtf syntax. code/comrak is also the program that I am using for parsing the markdown as I 
ran into errors using pulldown-cmark. 

---

1) Modifications are marked with the comment 'edited by erictepper'