from pathlib import Path

import scrapy


class BCRASpider(scrapy.Spider):
    name = "bcra"

    def start_requests(self):
        url = 'https://www.bcra.gob.ar/Estadisticas/EstadisSitiopublico/Proceso.aspx?selecciones=1222;1222;|&fechaDesde=01/02/2023&fechaHasta=01/03/2023'
        
        print("Esta es la url"+url)

    """def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'bcra-{page}.html'
        Path(filename).write_bytes(response.body)
        #self.log(f'Saved file {filename}')
        #print("esta es la página"+page)
        #print("este es el nombre de archivo"+filename)
        #print(response.xpath('//*[@id="GrdResultados"]/tbody/tr[7]/td[2]')) """

    def parse(self, response):

        trs = response.xpath('//table[@id="GrdResultados"]//td')

        #if trs:
            #items = []
        for tr in trs:
            print(tr)
                #print tr.xpath('td[2]//text()').extract()
            """
                item = {
                    "Name": tr.xpath('td[1]//text()').extract(),
                    "Position": tr.xpath('td[2]//text()').extract(),
                    "Office": tr.xpath('td[3]//text()').extract(),
                    "Age": tr.xpath('td[4]//text()').extract(),
                    "Start_Date": tr.xpath('td[5]//text()').extract(),
                    "Salary": tr.xpath('td[6]//text()').extract()
                }
                items.append(item)"""


            #x = pd.DataFrame(items, columns=['Name','Position','Office','Age',
                #'Start_Date','Salary'])