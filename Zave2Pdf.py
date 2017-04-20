#! /usr/bin/env python

import os, sys, zipfile, shutil
import xml.etree.ElementTree as ET
from reportlab.pdfgen import canvas
from pdfrw import PdfReader, PdfWriter, PageMerge

def usage():
    print "\nMain usage is;"
    print "    Zave2Pdf.py -zave input/folder/file.zave"
    print "\nIn order to specify saving file directory, use;"
    print "    Zave2Pdf.py -zave input/folder/file.zave -s save/path/file.pdf\n"

parameters = sys.argv[1:]

if not parameters.index("-zave")+1:
    print parameters
    print "you should indicate the zave file"
    usage()
    exit()
else:
    url = parameters[parameters.index("-zave") + 1]
    zave = zipfile.ZipFile(url, "r")
    url = os.path.dirname(url) + "/ZaveExtractedFiles"
    os.mkdir(url)
    zave.extractall(url)

try:
    if parameters.index("-s")+1:
        save = parameters[parameters.index("-s") + 1]
except:
    save = os.path.dirname(url)+"/issue.pdf"

if not os.path.isdir(url+"/Zave2PDFpages/"):
    os.mkdir(url+"/Zave2PDFpages/")

tree = ET.parse(url+ "/magazine.xml")

pages = tree.findall("articles/article/layouts/layout/page")
cnt = 1
items=[]

def addmedia(kind):
    for i in kind:
        try:
            if i.attrib["isButton"]:
                """Buttons couldn't be drawn"""
                pass
        except:
            file = i.find("fileSource").attrib["path"]

            if file[-4:-3] == ".":
                x = i.attrib["x"]
                y = i.attrib["y"]
                height = i.attrib["height"]
                width = i.attrib["width"]
                items.append([int(x), int(y), int(height), int(width), file])

print "\npage preparation ",
for page in pages:
    try:
        images = page.findall("image")
    except:
        images = False

    try:
        pdfs = page.findall("pdf")
    except:
        pdfs = page.find("pdf")

    if images:
        addmedia(images)

    sizes = page.attrib
    sizes = [int(sizes["width"]), int(sizes["height"])]

    c = canvas.Canvas(url+"/Zave2PDFpages/page"+str(cnt)+".pdf")
    c.setPageSize((sizes[0], sizes[1]))

    if items:
        for i in items:
            """
            x: i[0] y: i[1]
            w: i[3] h: i[2]
            """
            c.drawImage((url+"/"+i[4]), (i[0]), (sizes[1]-i[2]-i[1]), i[3], i[2], mask="auto")
    else:
        c.showPage()

    if page.find("subLayout") is not None: #Special Page
        sub = page.find("subLayout")
        if sub.attrib["scrollDirection"] == "2":
            width = int(sub.attrib["width"])
            height = int(sub.attrib["height"])
            x = int(sub.attrib["x"]) + width/2
            y = int(sizes[1]) - int(sub.attrib["y"]) - height/2
            c.drawCentredString(x, y, "You can view the content at the following page")
            print "|#|",

    c.save()
    items=[]
    addmedia(pdfs)
    current_page = PdfReader(url+"/Zave2PDFpages/page" + str(cnt) + ".pdf")

    for i in items[:]:
        pdf_media_file = PdfReader(url+"/" + i[4])
        pdf_media = PageMerge().add(pdf_media_file.pages[0])[0]
        pdf_media.x = i[0]
        pdf_media.y = sizes[1]-i[2]-i[1]
        pdf_media.w = i[2]
        pdf_media.h = i[3]

        PageMerge(current_page.pages[0]).add(pdf_media).render()
        PdfWriter().write((url+"/Zave2PDFpages/page"+str(cnt)+".pdf"), current_page)

    items = []

    sublayouts = page.findall("subLayout/internalSubLayout/subLayout/pages/page")
    if sublayouts:
        for sublayout in sublayouts:
            pages.insert(cnt,sublayout)

    if cnt % 5 == 0:
        sys.stdout.write("#")
        sys.stdout.flush()
    cnt = cnt + 1

print "\n\n" + str(cnt - 1) + " pages are being merged..."

writer = PdfWriter()
for i in range(1, cnt):
    writer.addpages(PdfReader(url+"/Zave2PDFpages/page"+str(i)+".pdf").pages)

writer.write(save)

print "\npreparing document"
print "\ndeleting temporary files and folders"
shutil.rmtree(url)

print "\nfile saved: "+ save
