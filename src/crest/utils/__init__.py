from selenium.webdriver.remote import webdriver


def define_absolute_xpath_fn(driver: webdriver.WebDriver):
    return driver.execute_script(
        """
window.absoluteXPath = function(element) {
    var comp, comps = [];
    var parent = null;
    var xpath = '';
    var getPos = function(element) {
        var position = 1, curNode;
        if (element.nodeType == Node.ATTRIBUTE_NODE) {
            return null;
        }
        for (curNode = element.previousSibling; curNode; curNode = curNode.previousSibling) {
            if (curNode.nodeName == element.nodeName) {
                ++position;
            }
        }
        return position;
    }
    if (element instanceof Document) {
        return '/';
    }
    for (
        ;
        element && !(element instanceof Document);
        element = element.nodeType == Node.ATTRIBUTE_NODE ? element.ownerElement : element.parentNode
    ) {
        comp = comps[comps.length] = {};
        switch (element.nodeType) {
        case Node.TEXT_NODE:
            comp.name = 'text()';
            break;
        case Node.ATTRIBUTE_NODE:
            comp.name = '@' + element.nodeName;
            break;
        case Node.PROCESSING_INSTRUCTION_NODE:
            comp.name = 'processing-instruction()';
            break;
        case Node.COMMENT_NODE:
            comp.name = 'comment()';
            break;
        case Node.ELEMENT_NODE:
            comp.name = element.nodeName;
            break;
        }
        comp.position = getPos(element);
    }
    for (var i = comps.length - 1; i >= 0; i--) {
        comp = comps[i];
        xpath += '/' + comp.name.toLowerCase();
        if (comp.position !== null) {
            xpath += '[' + comp.position + ']';
        }
    }
    return xpath;
};""")


def define_css_path_fn(driver: webdriver.WebDriver):
    return driver.execute_script("""
window.cssPath = function (el) {
    if (!(el instanceof Element)) return;
    var path = [];
    while (el.nodeType === Node.ELEMENT_NODE) {
        var selector = el.nodeName.toLowerCase();
        if (el.id) {
            selector += "#" + el.id;
            path.unshift(selector);
            break;
        } else {
            var sib = el, nth = 1;
            while (sib = sib.previousElementSibling) {
                if (sib.nodeName.toLowerCase() == selector) nth++;
            }
            if (nth != 1) selector += ":nth-of-type("+nth+")";
        }
        path.unshift(selector);
        el = el.parentNode;
    }
    return path.join(" > ");
}""")
