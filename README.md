#MDViewer for Mac OS X

The MDViewer is a markdown previewer which is implemented in python and can be used in Mac OS X or
Unix system directly. For the Linux and Windows, it has to be adapted in monitoring your markdown 
file changes. 

The MDViewer is independent of your text editor so that you can use whichever text editor you like 
to edit your markdown file. 

The MDViewer simply waits for the save actions in the markdown file you are editing, and whenever 
the changes are saved, the MDViewer transforms markdown into html and display it in your web 
browser. 

## Introduction

MDViewer uses python markdown for transforming markdown into html and use python Jinja template engine 
for rendering the markdown content. 

For refreshing the browser automatically, I use the html meta data for refreshing 
your browser frequently so that you are able to see the changes directly. 

I use python select module for monitoring the file saved event. This module is available
for Mac OS X and Unix system so that the Linux and Windows users have to implement your 
own monitoring service. 

For your personalised look and feel, you can change the preview theme in the base.html by 
adding your css files. Since the browser will refresh your file frequently, it is 
recommended to use the css and javascript files locally.


## Installation


##Usage

