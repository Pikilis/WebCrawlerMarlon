import scrapy

class NestleBolosSpider(scrapy.Spider):
    name = "Bolo"
    start_urls = ["https://www.receitasnestle.com.br/nossas-receitas/receitas-bolos?p=1"]

    def parse(self, response):
        # Seleciona todas as receitas da página
        receitas = response.css('a.recipes__card')

        # Extrai os títulos e links das receitas
        for receita in receitas:
            titulo = receita.css('h3.name::text').get().strip()
            link = response.urljoin(receita.css('::attr(href)').get())

            # Salva cada receita
            yield {
                'titulo': titulo,
                'link': link
            }

        # Verifica se há mais páginas
        current_page_number = int(response.url.split("p=")[-1])
        next_page_number = current_page_number + 1
        next_page_url = f"https://www.receitasnestle.com.br/nossas-receitas/receitas-bolos?p={next_page_number}"

        # Condição de parada: verifica o número de receitas e a existência de um elemento específico
        # (ajuste o seletor 'div.no-results' conforme necessário)
        num_receitas = len(receitas)
        if num_receitas >= 5 and not response.css('div.no-results'):
            yield scrapy.Request(url=next_page_url, callback=self.parse)
        else:
            self.logger.info(f"Fim da paginação na página {current_page_number}")