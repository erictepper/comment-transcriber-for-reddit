// Copyright 2015 Google Inc. All rights reserved.
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
// THE SOFTWARE.

//! Command line tool to exercise pulldown-cmark.

extern crate getopts;

extern crate pulldown_cmark;

use pulldown_cmark::Parser;
use pulldown_cmark::{Options, OPTION_ENABLE_TABLES, OPTION_ENABLE_FOOTNOTES};
use pulldown_cmark::html;

use std::env;
use std::io;
use std::io::{Read, Write};
use std::path::Path;
use std::fs::File;

fn main() { // edited by erictepper
// edited by erictepper
} // edited by erictepper

fn render_html(text: &str, opts: Options) -> String {
    let mut s = String::with_capacity(text.len() * 3 / 2);
    let p = Parser::new_ext(text, opts);
    html::push_html(&mut s, p);
    s
}
