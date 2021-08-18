

from bs4 import BeautifulSoup

class Extractor:


    def relevant_rows(self,tag):
        return tag.has_attr('class') and tag.has_attr('data-id') and tag.has_attr('tabindex') and tag.has_attr('onclick')
    
    def _format_output(self, textlines):
        results = []
        index = 0
        while index + 1 < len(textlines):
            results.append(textlines[index].replace('\n',' ') + '\n\t' + textlines[index+1].replace('\n', ' '))
            index += 2

        return str.join('\n\n', results)

    def _get_text_lines(self, soup):
        textlines = []
        lines = soup.find_all(self.relevant_rows)
        textlines = [line.get_text() for line in lines]
        return [str(line).strip() for line in textlines]

    def extract_schedule(self, page):
        soup = BeautifulSoup(page, "html.parser")

        textlines = self._get_text_lines(soup)

        output = self._format_output(textlines)
        
        return output