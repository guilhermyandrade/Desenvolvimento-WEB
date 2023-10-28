### Objetivo da API

Uma oficina está precisando melhorar o processo de fluxo de veículos dentro da oficina. Para isso, ela precisa de uma API REST para as seguintes operações: CRUD (Create, Retrieve, Update e Delete) do registro de manutenção, contendo os dados do veículo, nome do cliente, nome do mecânico e data e hora de chegada do veículo. Deve ter uma operação para atualizar o horário de finalização da manutenção. Deve listar todos os veículos que estão em manutenção na oficina no momento. Por fim deve permitir excluir uma manutenção que foi incluída, mas que ainda não foi finalizada**. Os dados devem ser gravados em memória e vão existir enquanto a aplicação existir.

**Requisitos da API**

- Deve retornar os dados do veículo, nome do cliente, nome do mecânico e data e hora de chegada do veículo
- Operação para atualizar o horário de finalização da manutenção
- Listar todos os veículos que estão em manutenção na oficina no momento
- Excluir uma manutenção que foi incluída, mas que ainda não foi finalizada
- Dados devem ser gravados em memória e vão existir enquanto a aplicação existir

### Métodos POST

**create_manutencao  :  Cria um registro de manutenção.**

- Exemplo de requisição:

        URL da requisição: http://127.0.0.1:8000/create_manutencao

        Body - raw - JSON:
        {
            "nome_mecanico": "Michael Jackson",
            "nome_cliente": "Rodrigo Farias",
            "problema": "Motor morre do nada",
            "nome_veiculo": "Palio 2010",
            "placa_veiculo": "JBK-3472"
        }
    
- Retorno:

        {
            "message": "Operação executada com sucesso.",
            "id_manutencao_criada": "6929d781-11c6-492f-8636-7bbab7e3b756"
        }

<hr>

### Métodos GET

**get_manutencao  :  Obtém os registros de manutenções agendadas.**

- Exemplo de requisição:

        URL da requisição: http://127.0.0.1:8000/get_manutencao

- Retorno:

        [
            {
                "id_manutencao": "6929d781-11c6-492f-8636-7bbab7e3b756",
                "data_hora_inicio_manutencao": null,
                "data_hora_fim_manutencao": null,
                "data_hora_chegada_veiculo": null,
                "data_hora_criacao_registro": "27/10/2023 21:07:40",
                "nome_mecanico": "Michael Jackson",
                "nome_cliente": "Rodrigo Farias",
                "veiculo": {
                    "nome": "Palio 2010",
                    "placa": "JBK-3472"
                },
                "problema": "Motor morre do nada",
                "status": "Pendente"
            }
        ]

<hr>

**get_veiculos_em_manutencao  :  Obtém os veículos onde o status da manutenção é "Em progresso"**

- Exemplo de requisição:

        URL da requisição: http://127.0.0.1:8000/get_veiculos_em_manutencao

- Retorno:

        [
			{
				"nome": "Palio 2010",
				"placa": "JBK-3472"
			}
		]

<hr>

### Métodos PUT

**update_dh_inicio_manutencao  :  Atualiza a data e hora de início da manutenção.**


- Exemplo de requisição:

        URL da requisição: http://127.0.0.1:8000/update_dh_inicio_manutencao

        Body - raw - JSON:

        {
            "id_manutencao": "6929d781-11c6-492f-8636-7bbab7e3b756",
            "data_hora_inicio_manutencao": "27/10/2023 13:15:00"
        }

- Retorno:

        {
            "message": "Operação executada com sucesso."
        }

<hr>

**update_dh_fim_manutencao  :  Atualiza a data e hora do fim da manutenção.**

- Exemplo de requisição:

        URL da requisição: http://127.0.0.1:8000/update_dh_fim_manutencao

        Body - raw - JSON:

        {
            "id_manutencao": "6929d781-11c6-492f-8636-7bbab7e3b756",
            "data_hora_fim_manutencao": "27/10/2023 14:37:00"
        }

- Retorno:

        {
            "message": "Operação executada com sucesso."
        }

<hr>

**update_dh_chegada_veiculo  :  Atualiza a data e hora da chegada do veículo.**

- Exemplo de requisição:

        URL da requisição: http://127.0.0.1:8000/update_dh_chegada_veiculo

        Body - raw - JSON:

        {
            "id_manutencao": "6929d781-11c6-492f-8636-7bbab7e3b756",
            "data_hora_chegada_veiculo": "27/10/2023 11:45:00"
        }

- Retorno:

        {
            "message": "Operação executada com sucesso."
        }

<hr>

### Métodos DELETE

**delete_manutencao  :  Deleta um registro de manutenção.**

- Exemplo de requisição:

        URL da requisição: http://127.0.0.1:8000/delete_manutencao

        Body - raw - JSON:

        {
            "id_manutencao": "6929d781-11c6-492f-8636-7bbab7e3b756"
        }

- Retorno:

        {
            "message": "Operação executada com sucesso."
        }