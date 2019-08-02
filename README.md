# reddit-comment-transcriber
A script that converts a thread of Reddit comments to a rich text file. 

code/snoomark.py, code/comrak/, and code/pulldown-cmark/ are all taken from https://github.com/zeantsoi/snoomark-binding for 
use converting markdown to .rtf formatting. code/comrak/src/html.rs has been edited by me to change the output of the 
parser from html tags to .rtf syntax. 