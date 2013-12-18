from jinja2 import Environment, FileSystemLoader
import select
import markdown
import codecs
import os
import sys

#This script will monitor the markdown file, when the file is changed, the script
#call the Markdown.pl and integrate the output to the Jinja2 template for viewing 
#in the browser. This script is written for usage in the Mac OS.

#The purpose of using select and kqueue is to avoid the loop check sleep
#pattern. This script will be blocked until the system inform it that
#some changes have happened in the file.

#O_EVTONLY is defined as 0x8000 in the OS X header files.
#kqueue funcionality in watchdog for Mac OS
#https://github.com/gorakhargosh/watchdog/blob/master/src/watchdog/observers/kqueue.py
#documentation for select
#http://docs.python.org/2.7/library/select.html


def md_to_html(filename, rtime):
    html_filename = "%s.html"
    name, filename_extension = filename.split(".")
    input_file = codecs.open(filename, mode="r", encoding="utf-8")
    text = input_file.read()
    html = markdown.markdown(text)
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),trim_blocks=True)
    renderVar = {"content":html, "rtime":rtime}
    html = j2_env.get_template('base.html').render(renderVar)
    output_file = codecs.open(html_filename % name, "w", encoding="utf-8", errors="xmlcharrefreplace")
    output_file.write(html)
    input_file.close()
    output_file.close()

def main():

    filename = "test.md"
    rtime = 2
    O_EVTONLY = 0x8000
    fd = os.open(filename, O_EVTONLY)
    kq = select.kqueue()
    KQ_FILTER = select.KQ_FILTER_VNODE
    KQ_EV_FLAGS = select.KQ_EV_ADD | select.KQ_EV_ENABLE | select.KQ_EV_CLEAR
    KQ_FFLAGS = select.KQ_NOTE_WRITE | select.KQ_NOTE_EXTEND
    event = [select.kevent(fd, filter=KQ_FILTER, flags=KQ_EV_FLAGS, fflags=KQ_FFLAGS)]
    try:
        while True:
            print "waiting for events"
            #This call will block till the write or extend events occur
            r_events = kq.control(event,1,None)
            for ev in r_events:
                if ev.fflags & select.KQ_NOTE_WRITE:
                    #print "write event occur"
                    md_to_html(filename, rtime)
    except KeyboardInterrupt:
        print "\n Keyboard Interruption with Ctrl C, \n finishing..."
        kq.close()
        os.close(fd)
        print "finished"

if __name__=="__main__":
    sys.exit(main())
