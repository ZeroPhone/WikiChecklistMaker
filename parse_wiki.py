from collections import OrderedDict
from lxml import html as xhtml
import requests
import shutil
import sys
import os


default_url = "https://wiki.zerophone.org/index.php/Sourcing_ZeroPhone_parts"

def get_wiki_page(url):
    req = requests.get(url)
    assert(req.status_code == 200)
    return req.text

def get_page_contents(url = default_url):
    page_html = get_wiki_page(url)
    tree = xhtml.fromstring(page_html)
    content_xpath = "//div[@id='mw-content-text']"
    content_element = tree.xpath(content_xpath)[0]
    return content_element

def get_parts(contents):
    parts = OrderedDict()
    toc = contents.xpath("//div[@id='toc']")[0]
    #categories = toc.xpath("ul/li")
    return parse_categories(toc, contents)

def parse_categories(start, root):
    categories = []
    for c in start.xpath("ul/li"):
        s = parse_categories(c, root) #subcategories
        h = get_category_header(c) #header
        if not s:
            q, n = get_category_quantity_and_notes(c, root) #quantity
        else: #category has subcategories, so it does not have a quantity by itself
            q = None
        d = {"name":h}
        if q: d["quantity"] = q
        if s: d["subcategories"] = s
        if n: d["notes"] = n
        categories.append(d)
    return categories

def get_category_header(c):
    headers = c.xpath("a/span[@class='toctext']")
    assert(len(headers) == 1) #should only be one header
    return headers[0].text

def get_part_description(header_xpath, root):
    return root.xpath("{}/following::p".format(header_xpath))[0]

def get_category_quantity_and_notes(c, root, default_quantity=1):
    quantity = 1 #Default quantity
    notes = []
    links = c.xpath('a')
    assert(len(links) == 1) #should only be one link
    link_id = links[0].get("href")
    assert(link_id.startswith("#")) #should be an anchor
    link_id = link_id.lstrip('#')
    header_xpath = "//span[@id='{}']".format(link_id)
    description = get_part_description(header_xpath, root)
    bold_elements = description.xpath("b")
    for el in bold_elements: 
        #We expect a <b> element containing "Quantity: X"
        start_string = "Quantity: "
        if el.text.startswith(start_string):
            quantity = el.text[len(start_string):]
        #We might also have a <b> element containing "Not required"
        #In the future, there might be some other notes
        possible_notes = ["Not required"]
        if el.text.strip() in possible_notes:
            notes.append(el.text.strip())
    return (quantity, notes)
    import pdb; pdb.set_trace()


if __name__ == "__main__":
    import pprint
    pprint.pprint(get_parts(get_page_contents()))
