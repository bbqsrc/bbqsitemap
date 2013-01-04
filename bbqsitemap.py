import gzip

from xml.sax.saxutils import escape

START = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
END = '</urlset>'

class Sitemap:
    def __str__(self):
        return START + "".join(self.urls) + END

    def __init__(self):
        self.urls = []
        self.size = len(START) + len(END)

    def add(self, url):
        url = "<url><loc>%s</loc></url>" % escape(url)

        if len(url) + self.size > 10485760:
            raise Exception("Sitemap would be over 10MB!")
        else:
            self.size += len(url)

        self.urls.append(url)

    def save(self, path, compress=True):
        if compress:
            f = gzip.open(path, 'wb')
        else:
            f = open(path, 'wb')
        f.write(str(self).encode('utf-8'))
        f.close()
