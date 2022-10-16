#! /bin/env python3
import sys, pikepdf
from PIL import Image
from PIL.ExifTags import TAGS
from colorama import Fore

cyan = Fore.CYAN
white = Fore.WHITE


def get_pdf_metadata(pdf_file):
    # read the pdf file
    pdf = pikepdf.Pdf.open(pdf_file)
    # .docinfo attribute contains all the metadata of
    # the PDF document
    return dict(pdf.docinfo)

def get_image_metadata(image_file):
    # read the image data using PIL
    image = Image.open(image_file)
    # extract other basic metadata
    info_dict = {
        "Filename": image.filename,
        "Image Size": image.size,
        "Image Height": image.height,
        "Image Width": image.width,
        "Image Format": image.format,
        "Image Mode": image.mode,
        "Image is Animated": getattr(image, "is_animated", False),
        "Frames in Image": getattr(image, "n_frames", 1)
    }

    # extract EXIF data
    exifdata = image.getexif()
    
    # iterating over all EXIF data fields
    for tag_id in exifdata:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        # decode bytes
        if isinstance(data, bytes):
            data = data.decode()
        
        # print(f"{tag:25}: {data}")
        info_dict[tag] = data

    return info_dict

def get_media_metadata(media_file):
    # uses ffprobe command to extract all possible metadata from media file
    ffmpeg_data = ffmpeg.probe(media_file)["streams"]
    tt_data = TinyTag.get(media_file).as_dict()
    # add both data to a single dict
    return {**tt_data, **ffmpeg_data}

def help():
    print(f"Usage : {sys.argv[0]} [file-path]")
    
if __name__ == "__main__":
    try:
        file = sys.argv[1]
    except:
        help()
        exit()

    if file.endswith(".pdf"):
        metadata = get_pdf_metadata(file)
        for i in metadata:
            j = str(i)
            j = j.replace("/", "")
            print(f"{cyan}{j} {white}: {metadata[i]}")

    elif file.endswith(".jpg"):
        metadata = get_image_metadata(file)
        for i in metadata:
            j = str(i)
            j = j.replace("/", "")
            print(f"{cyan}{j} {white}: {metadata[i]}")
    else:
        metadata = get_media_metadata(file)
        for i in metadata:
            j = str(i)
            j = j.replace("/", "")
            print(f"{cyan}{j} {white}: {metadata[i]}")