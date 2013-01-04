import gzip

from xml.sax.saxutils import escape

class Sitemap:
    START = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    END = '</urlset>'
    URL = "<url><loc>%s</loc></url>"
    
    def __str__(self):
        return self.START + "".join(self.urls) + self.END

    def __init__(self):
        self.urls = []
        self.size = len(self.START) + len(self.END)

    def add(self, url):
        url = self.URL % escape(url)
        
        if len(self.urls) >= 50000:
            raise Exception("%s would have more than 50,000 URLs!" %
                    self.__class__.__name__)
        elif len(url) + self.size > 10485760:
            raise Exception("%s would be over 10MB!", self.__class__.__name__)
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


class SitemapIndex(Sitemap):
    START = '<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    END = '</sitemapindex>'
    URL = '<sitemap><loc>%s</loc></sitemap>'


class SitemapManager:
    def __init__(self, host):
        if not host.endswith('/'):
            host += '/'
        self.host = host
        self.index = SitemapIndex()
        self.sitemaps = [Sitemap()]

    def add(self, url):
        try:
            self.sitemaps[-1].add(url)
        except:
            self.sitemaps.append(Sitemap())
            self.add(url)

    def save(self):
        for n, sitemap in enumerate(self.sitemaps):
            fn = "sitemap%s.xml.gz" % n
            sitemap.save(fn)
            self.index.add(self.host + fn)
        self.index.save('sitemapindex.xml.gz')

