# Reddit Comment Transcriber
A program that converts a thread of Reddit comments to a rich text file. 

code/snoomark.py, code/comrak/, and code/pulldown-cmark/ are taken from https://github.com/zeantsoi/snoomark-binding, 
https://github.com/zeantsoi/comrak, and https://github.com/zeantsoi/pulldown-cmark respectively for use converting 
markdown to .rtf formatting (from what I can tell, these cited projects are what are officially used for parsing 
Reddit's markdown and converting it to html). code/comrak/src/html.rs has been edited by me to change the output of the 
parser from html tags to .rtf syntax. code/comrak is also the program that I am using for parsing the markdown as I ran 
into errors using pulldown-cmark. 