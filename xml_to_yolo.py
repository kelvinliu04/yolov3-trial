import os 
import glob
import xml.etree.ElementTree as ET

names_dict = {'background':0, 'plate':1}

def parse_xml(path):
    tree = ET.parse(path)
    img_name = path.split('.xml')[0] + '.jpg'
    
    text = '{}'.format(img_name)
    objects = [img_name]

    for obj in tree.findall('object'):
        difficult = obj.find('difficult').text
        if difficult == '1':
            continue
        name = obj.find('name').text
        bbox = obj.find('bndbox')
        xmin = bbox.find('xmin').text
        ymin = bbox.find('ymin').text
        xmax = bbox.find('xmax').text
        ymax = bbox.find('ymax').text

        class_id = str(names_dict[name])
        objects.extend([xmin, ymin, xmax, ymax, class_id])
        text = text + ' {},{},{},{},{}'.format(xmin, ymin, xmax, ymax, class_id)
        
    text = text + '\n'
    if len(objects) > 1:
        return text
    else:
        return None
    

def gen_txt(txt_path, imgs_path):
    cnt = 0
    img_names = glob.glob(imgs_path)
    f = open(txt_path, 'w')
    for img_name in img_names:
        img_name = '.' + img_name.split('.')[1]
        xml_path = img_name + '.xml'
        text = parse_xml(xml_path)
        f.write(text)
        
    f.close()

train_imgs_path = './data/dataset/train/*.jpg'
val_imgs_path = './data/dataset/val/*.jpg'
gen_txt('train.txt', train_imgs_path)
gen_txt('val.txt', val_imgs_path)