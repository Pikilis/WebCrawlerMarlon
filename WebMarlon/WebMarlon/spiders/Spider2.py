import scrapy

class DeliciaBolosSpider(scrapy.Spider):
    name = "Bolinho"
    start_urls = ["https://www.delicia.com.br/receitas/bolos/"]

    def parse(self, response):
        # Seleciona todos os links de receitas na página
        receitas = response.css('a[title]')

        # Extrai o título e o link de cada receita
        for receita in receitas:
            titulo = receita.css('::attr(title)').get()
            link = receita.css('::attr(href)').get()

            # Verifica se o título e o link foram extraídos corretamente
            if titulo and link:
                yield {
                    'titulo': titulo.strip(),
                    'link': response.urljoin(link)
                }

        # Procura o botão "VEJA MAIS RECEITAS" para pegar a quantidade de páginas
        veja_mais = response.css('a.call-to-action.paginate')
        if veja_mais:
            total_pages = int(veja_mais.attrib.get('data-pages', 1))

            # Inicia a paginação percorrendo de 2 até total_pages
            for page in range(2, total_pages + 1):
                next_page_url = f"https://www.delicia.com.br/receitas/bolos/?page={page}"
                yield scrapy.Request(url=next_page_url, callback=self.parse)
        else:
            self.logger.info("Fim da paginação.")
