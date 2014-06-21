# Flask Multi Upload Demo

This is a quick example of a Python/Flask app I wrote while figuring out how to
make an HTML5 multi-file uploader script.

This app just presents an HTML form full of the usual types of input elements
(text boxes, checkboxes, etc.), and a multi-file input box, and an HTML5
drag/drop target for dragging files from your PC into the page.

It demonstrates that you can combine a multi-file upload form along with other
form data (i.e. letting a user choose album details to upload the pictures into).
There's also a live progress bar that tells you the current progress of the
upload. It doesn't break it down by individual file though, to keep things simpler.

It's backwards compatible and also works with clients that have scripts disabled.
The same endpoint is used on the back-end to handle the form post and file
upload; when the Ajax calls the endpoint, the Flask app returns a JSON response
including the "unique ID" chosen for the upload, and then the JavaScript on
the front-end initiates a redirect. With scripts disabled (so that the form will
`POST` directly to the back-end), a normal HTTP redirect is given to the final
results page.

This code demonstrates the bare essentials for how to get a multi-uploader to
work using HTML5, JavaScript and jQuery -- without needing Flash or Java.
It works in most modern browsers and Internet Explorer 10+.

It's only 184 lines of JavaScript and 80 lines of Python.

# License

This is released in the public domain in the hopes that it will be generally
useful to other developers. I wrote this just to see how to do it and to use
as reference in other projects.
