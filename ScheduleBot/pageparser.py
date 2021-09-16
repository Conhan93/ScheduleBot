from bs4 import BeautifulSoup

class PageParser:
    """ extracts text and formats schedule text from page """

    def schedule_rows(self,tag):
        return tag.has_attr('class') and tag.has_attr('data-id') and tag.has_attr('tabindex') and tag.has_attr('onclick')
    
    def _get_text_lines(self, soup):
        lines = soup.find_all(self.schedule_rows)
        textlines = [line.get_text() for line in lines]

        return [list(filter(None, line.split('\n'))) for line in textlines]

    def extract_schedule(self, page):
        soup = BeautifulSoup(page, "html.parser")

        entries = self._get_text_lines(soup)

        return entries