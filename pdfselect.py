"""
pdfsleect.py 

Sends pdf in a folder to amazon textract api  ...
"""
import os
import glob
import boto3


class Processor:
    def __init__(self):
        self.standard_size = [1280, 144]
        self.folder = input("Select input folder: ").strip()
        self.find_image_files()
        print("Found", len(self.files), "in folder", self.folder, ", processing...")
        self.process_files()

    def find_image_files(self):
        files = sorted(glob.glob(os.path.join(self.folder, "*.pdf")))
        files = [filename for filename in files 
           if not filename.endswith('resize.pdf')]
        print("Found pdf files")
        for filename in files:
            print(filename)
        self.files = files

    def process_files(self):
        if len(self.files) == 0:
            return 
        self.client = boto3.client('textract')
        for filename in self.files:
            self.process_file(filename)

    def process_file(self, filename):
        """
        Sends the image to textract and waits for the result
        """
        print("Processing pdf", filename)
        #process using image bytes
        with open(filename, 'rb') as filein:
            image_binary = filein.read() 
        response = self.client.detect_document_text(Document={'Bytes': image_binary})

if __name__ == "__main__":
    Processor()

     
