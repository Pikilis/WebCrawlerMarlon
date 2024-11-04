import scrapy

class BolosSpider(scrapy.Spider):
    name = 'boulos'
    start_urls = [
        'https://www.receitasnestle.com.br/nossas-receitas/receitas-bolos?p=1',
        'https://www.delicia.com.br/receitas/bolos/'
    ]

    def parse(self, response):
        # Verifica de qual site está sendo feita a coleta
        if "receitasnestle" in response.url:
            yield from self.parse_nestle(response)
        elif "delicia" in response.url:
            yield from self.parse_delicia(response)

        # Extraindo link da próxima página
        if "receitasnestle" in response.url:
            proxima_pagina = response.css('a#load_more::attr(href)').get()
            if proxima_pagina:
                yield response.follow(proxima_pagina, self.parse)
        elif "delicia" in response.url:
            carregar_mais = response.css('a.call-to-action.paginate::attr(href)').get()
            if carregar_mais:
                next_page_url = response.urljoin(carregar_mais)
                yield response.follow(next_page_url, self.parse)

    def parse_nestle(self, response):
        # Seleciona todas as receitas na página
        receitas = response.css('a.recipes__card')

        # Extrai o título e o link de cada receita
        for receita in receitas:
            titulo = receita.css('h3.name::text').get()
            link = receita.css('::attr(href)').get()

            # Verifica se o título e o link foram extraídos corretamente
            if titulo and link:
                yield {
                    'titulo': titulo.strip(),
                    'link': response.urljoin(link)
                }

    def parse_delicia(self, response):
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

        # Verificar se há um botão "Carregar mais" e seguir o link se existir
        carregar_mais = response.css('a.call-to-action.paginate::attr(href)').get()
        if carregar_mais:
            next_page_url = response.urljoin(carregar_mais)
            yield response.follow(next_page_url, self.parse_delicia)