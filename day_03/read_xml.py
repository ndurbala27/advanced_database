import xml.etree.ElementTree as ET

xfile = 'country_data.xml'

tree = ET.parse(xfile)
root = tree.getroot()
# print(root)
# print(root.tag)
# print(root.attrib)

for child in root:
    # print(child.tag)
    # print(child.tag, child.attrib)  # Notice the output
    print(type(child.attrib))
    print(child.attrib)
    # print(f"{child.tag}: {child.attrib['name']}")
    print()