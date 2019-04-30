import os
import cv2
import glob
from lxml import etree
import xml.etree.cElementTree as ET
import pandas as pd

testPath="E:\\ooops\my\\images\\test"
trainPath="E:\\ooops\my\\images\\train"
def write_xml(folder, p, objects, tl, br, savedir):
    if not os.path.isdir(savedir):
        os.mkdir(savedir)

    image = cv2.imread(p)
    image= cv2.resize(image,(300,300),3)
    height, width, depth = image.shape

    annotation = ET.Element('annotation')
    # ET.SubElement(annotation, 'folder').text = folder
    # ET.SubElement(annotation, 'filename').text = p
    ET.SubElement(annotation, 'folder').text = folderdup
    ET.SubElement(annotation, 'filename').text = p
    ET.SubElement(annotation,'path').text = p
    ET.SubElement(annotation, 'segmented').text = '0'
    size = ET.SubElement(annotation, 'size')
    ET.SubElement(size, 'width').text = str(width)
    ET.SubElement(size, 'height').text = str(height)
    ET.SubElement(size, 'depth').text = str(depth)
    for obj, topl, botr in zip(objects, tl, br):
        ob = ET.SubElement(annotation, 'object')
        ET.SubElement(ob, 'name').text = obj
        ET.SubElement(ob, 'pose').text = 'Unspecified'
        ET.SubElement(ob, 'truncated').text = '0'
        ET.SubElement(ob, 'difficult').text = '0'
        bbox = ET.SubElement(ob, 'bndbox')
        ET.SubElement(bbox, 'xmin').text = str(topl[0])
        ET.SubElement(bbox, 'ymin').text = str(topl[1])
        ET.SubElement(bbox, 'xmax').text = str(botr[0])
        ET.SubElement(bbox, 'ymax').text = str(botr[1])

    xml_str = ET.tostring(annotation)
    root = etree.fromstring(xml_str)

    xml_str = etree.tostring(root, pretty_print=True)
    save_path = os.path.join(savedir, p.replace('jpg', 'xml'))

    with open(save_path, 'wb') as temp_xml:
        temp_xml.write(xml_str)


def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):

        tree = ET.parse(xml_file)

        root = tree.getroot()

        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )

            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df






if __name__ == '__main__':
#     """
#     for testing
#     """

    import json
    import os
    import cv2

    folde = "E:\ooops\my\images"
    folderdup = os.path.basename(os.path.normpath(folde))
    print(folderdup)

    import os


    folder = "E:\ooops\my\images"
    for i in os.listdir(folder):

        for root1, subdir, files in os.walk(folder):

            for files in os.listdir(root1):

                if files.endswith('.jpg'):
                    image = os.path.join(root1, files)
                    p = image
                    objects = ['trafficlight']
                    tl = [(10, 10)]
                    br = [(100, 100)]
                    savedir = 'annotations'
                    write_xml(folder, p, objects, tl, br, savedir)
    for i in [trainPath, testPath]:
        image_path = i


        folder = os.path.basename(os.path.normpath(i))
        # print(folder)
        xml_df = xml_to_csv(image_path)

        xml_df.to_csv('data/' + folder +'.csv', index=None)

