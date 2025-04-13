import xml.etree.ElementTree as ET

# Create the root node
root = ET.Element('people')

# Create one child element
person = ET.SubElement(root, "person")
person.attrib = {'name' : 'johnny'}
person.text =  "Here's Johnny!"

# Create the tree
tree = ET.ElementTree(root)

#Write to an xml file
tree.write('people.xml')