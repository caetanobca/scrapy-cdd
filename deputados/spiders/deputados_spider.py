import scrapy


class DeputadosSpiderSpider(scrapy.Spider):
    name = 'deputados_spider'

    def start_requests(self):
        file = open("lista_deputadas.txt", "r")
        deputadas = file.read().replace('"', '')
        deputadas_list = deputadas.split(',\n')
        file.close()

        file = open("lista_deputados.txt", "r")
        deputados = file.read().replace('"', '')
        deputados_list = deputados.split(',\n')
        file.close()


        for url in deputados_list:
            yield scrapy.Request(url=url, callback=self.parse, meta={"gender": "M"})

        for url in deputadas_list:
            yield scrapy.Request(url=url, callback=self.parse, meta={"gender": "F"})

        # yield scrapy.Request(url='https://www.camara.leg.br/deputados/141431', callback=self.parse, meta={"gender": "F"})

    def parse(self, response, **kwargs):
        result = self.get_gasto(response)
        result['nome'], result['data_nascimento'] = self.get_info(response)
        result['genero'] =  response.meta.get("gender")
        result['presenca_plenario'], result['ausencia_plenario'], result['ausencia_justificada_plenario'], result['presenca_comissao'], result['ausencia_comissao'], result['ausencia_justificada_comissao'] = self.get_presenca(response)
        result['salario_bruto'], result['quant_viagem']  = self.get_salario_viagens(response)
        
        yield result


    def get_info(self, response):
        data = response.css("ul.informacoes-deputado li::text").getall()
        return data[0][1:], data[4][1:]

    def get_presenca(self, response):
        data = response.css("dl.list-table__definition-list dd::text").getall()
        return (int(data[0].strip().split()[0]), int(data[1].strip().split()[0]), int(data[2].strip().split()[0]),
        int(data[3].strip().split()[0]), int(data[4].strip().split()[0]) ,int(data[5].strip().split()[0]))
    
    def get_gasto(self, response):
        gastos = []
        # print(response.css("div.gasto__col tbody td::text").getall())
        
        for i in response.css("div.gasto__col"):
            gastos.append(i.css("tbody td::text").getall())
        # print(gastos)

        gastos_par = [0,0,0,0,0,0,0,0,0,0,0,0]
        gastos_gab = [0,0,0,0,0,0,0,0,0,0,0,0]

        for i in range(12):
            if len(gastos[1]) >= (i * 3) + 1:
                gastos_par[i] = int(gastos[1][(i * 3) + 1].replace(".", "").replace(",", "")) / 100
            if len(gastos[3]) >= (i * 3) + 1:
                gastos_gab[i] = int(gastos[3][(i * 3) + 1].replace(".", "").replace(",", "")) / 100


        gastos_dict = {
            "gasto_total_par": int(gastos[0][1].replace(".", "").replace(",", "")) / 100,
            "gasto_jan_par": gastos_par[0],
            "gasto_fev_par": gastos_par[1],
            "gasto_mar_par": gastos_par[2],
            "gasto_abr_par": gastos_par[3],
            "gasto_maio_par": gastos_par[4],
            "gasto_junho_par": gastos_par[5],
            "gasto_jul_par": gastos_par[6],
            "gasto_agosto_par": gastos_par[7],
            "gasto_set_par": gastos_par[8],
            "gasto_out_par": gastos_par[9],
            "gasto_nov_par": gastos_par[10],
            "gasto_dez_par": gastos_par[11], 
            "gasto_total_gab": int(gastos[2][1].replace(".", "").replace(",", "")) / 100, 
            "gasto_jan_gab": gastos_gab[0], 
            "gasto_fev_gab": gastos_gab[1], 
            "gasto_mar_gab": gastos_gab[2], 
            "gasto_abr_gab": gastos_gab[3],
            "gasto_maio_gab": gastos_gab[4], 
            "gasto_junho_gab": gastos_gab[5], 
            "gasto_jul_gab": gastos_gab[6], 
            "gasto_agosto_gab": gastos_gab[7],
            "gasto_set_gab": gastos_gab[8], 
            "gasto_out_gab": gastos_gab[9], 
            "gasto_nov_gab": gastos_gab[10], 
            "gasto_dez_gab": gastos_gab[11], 
        }
        return gastos_dict

    

    def get_salario_viagens(self, response):
        salario = response.css("ul.recursos-beneficios-deputado-container li div.beneficio .beneficio__info::text").getall()[1].split()[1]
        salario = int(salario.replace(".", "").replace(",", "")) / 100

        viagens = int(response.css("ul.recursos-beneficios-deputado-container li div.beneficio .beneficio__info::text").getall()[-2])

        return (salario, viagens)