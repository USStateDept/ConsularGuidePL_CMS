from lxml.builder import E
from lxml import etree
from lxml.html.builder import CLASS
import json

DIV_CLASSES = ['phone', 'hours', 'place', 'mail', 'info', 'categories']

def prepend_text(parent, prev, text):
	if prev is not None:
		if prev.tail is not None:
			prev.tail += text
		else:
			prev.tail = text
	else:
		if parent.text is not None:
			parent.text += text
		else:
			parent.text = text


def fix(node, after):
	if node.tag == "div" and node.get('class') in DIV_CLASSES:
		return
	children = node.getchildren()
	new_after = after

	for child in children:
		if child.tag in ("div", "p", "h1", "h2", "ol", "ul", "img", "a"):
			prev = child.getprevious()

			text = ''
			if child.tag == 'a':
				text = "".join([x for x in child.itertext()])
				# no tags inside a button
				children = child.getchildren()
				for ch in children:
					child.remove(ch)
				child.text = text

				# if properly wrapped continue
				if len(node.getchildren()) == 1 and node.text is None and node.tag == 'p' and child.tail is None:
					continue

			if child.tail is not None:
				text += child.tail
			if text != '':
				prepend_text(node, prev, text)
				child.tail = None

			if child.tag != "a":
				new_after.addnext(child)
				new_after = child

				if child.tag != "div":
					fix(child, child)
			else:
				elt = etree.Element("p")
				elt.append(child)
				new_after.addnext(elt)
				new_after = elt

			if (not node.getchildren()) and (node.text is None):
				node.getparent().remove(node)
		else:
			fix(child, new_after)


def clean_content(data):
		# easy content fixes
		data = data.replace("&nbsp;", "\u00a0")

		root = etree.fromstring("<content>" + data + "</content>")

		# remove scripts - norton toolbar issue
		for element in root.xpath("//script"):
			element.getparent().remove(element)

		# remove local imgs
		for element in root.xpath("//img"):
			src = element.get('src')
			if src is None or src.startswith('file://'):
				element.getparent().remove(element)

		# remove comments
		for comment in root.xpath('//comment()'):
			comment.getparent().remove(comment)

		# strip spans
		etree.strip_tags(root, 'span')

		# strip nested strongs
		for element in root.xpath('//strong'):
			etree.strip_tags(element, 'strong')

		# tables to categories
		for element in root.xpath("//table"):
			etree.strip_tags(element, 'tbody')
			element.tag = 'div'
			element.set('class', 'categories')
			for item in element.getchildren():
				item.tag = 'div'
				item.set('class', 'citem')
				for i, child in enumerate(item.getchildren()):
					child.tag = 'div'
					if i == 0:
						child.set('class', 'cname')
					elif i == 1:
						child.set('class', 'ctext')
					else:
						child.getparent().remove(child)

		# strip paragraphs from lists
		for element in root.xpath("//li"):
			etree.strip_tags(element, 'p')
			etree.strip_tags(element, 'h1')
			etree.strip_tags(element, 'h2')

		# remove nested lists
		for element in root.xpath("//ul | //ol"):
			etree.strip_tags(element, 'ul', 'ol')

		# convert anchors to buttons
		for element in root.xpath("//a"):
			btnclass = element.get('class')
			url = element.get('href')
			if url is None and (btnclass is None or btnclass != 'btn'):
				element.getparent().remove(element)
				continue

			element.set('class', 'btn')
			if url is not None:
				del element.attrib['href']
				if url.startswith('mailto:'):
					url = url.replace('mailto:', '')
					text = "".join([x for x in element.itertext()])
					mail = E.div(E.div(text, CLASS("row")), E.div(url, CLASS("row")), CLASS("mail"))
					mail.set('data-address', url)
					mail.tail = element.tail
					parent = element.getparent()
					# prepend_text(parent, element.getprevious(), text)
					parent.replace(element, mail)
				elif url.startswith('http://') or url.startswith('https://'):
					element.set('data-url', url)
				else:
					element.set('data-url', 'http://' + url)

		# fix nested items
		children = root.getchildren()
		for child in children:
			fix(child, child)

		# fix info popups
		for element in root.xpath('//div[@class="longinfo"]'):
			children = element.getchildren()
			for child in children:
				fix(child, child)

		# fix empty divs
		for element in root.xpath('/content/div'):
			if element.get('class') not in DIV_CLASSES:
				element.getparent().remove(element)

		# reverse &nbsp;
		data = etree.tounicode(root)
		data = data.replace("\u00a0", "&nbsp;")
		return data


def clean_faq(data):
	faq_list = json.loads(data)

	for question in faq_list:
		question['answer'] = clean_content(question['answer'])

	return json.dumps(faq_list)