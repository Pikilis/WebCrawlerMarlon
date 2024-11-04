import scrapy

class NestleBolosSpider(scrapy.Spider):
    name = "Bolo"
    start_urls = ["https://www.receitasnestle.com.br/nossas-receitas/receitas-bolos?p=1"]

    def parse(self, response):
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

        # Verifica se há um botão "Mostrar mais" e obtém o link da próxima página
        next_page = response.css('a#load_more::attr(href)').get()
        if next_page:
            # Segue para a próxima página usando o link do botão "Mostrar mais"
            yield response.follow(next_page, callback=self.parse)
        else:
            self.logger.info("Fim da paginação.")
