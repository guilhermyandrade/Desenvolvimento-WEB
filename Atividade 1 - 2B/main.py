import json
from typing import List
from uuid import uuid4
from fastapi import FastAPI, Request
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()  # Variável que contém o aplicativo

# Observações:
# 1) Em python, há um padrão de organização onde todas as classes devem ter nome com primeira letra maiúscula.
# 2) Os nomes das variáveis costumam ser separados pelo caracter underline ( "_" ).
# 3) Os nomes das rotas são os mesmos nomes dos métodos para facilitar a interpretação do código e da API.
# 4) Variáveis contendo prefixo "arm" são usadas para armazenar os dados


class Manutencao(BaseModel):  # Estrutura dos dados da manutenção

    id_manutencao: str

    data_hora_inicio_manutencao: str = None
    data_hora_fim_manutencao: str = None    
    data_hora_chegada_veiculo: str = None

    data_hora_criacao_registro: str = None

    nome_mecanico: str
    nome_cliente: str
    
    veiculo: dict
    
    problema: str

    if data_hora_fim_manutencao == None and data_hora_inicio_manutencao == None:  # Se inicio e fim forem igual a "None", o status recebe "Pendente"
        __variavel_status = 'Pendente'

    elif data_hora_fim_manutencao != None:  # Se a variável dh_fim_manutencao for diferente de None, status recebe "Concluído"
        __variavel_status = 'Concluído'

    elif data_hora_inicio_manutencao != None:  # Se a variável dh_inicio_manutencao for diferente de "None", status recebe "Em progresso"
        __variavel_status = 'Em progresso'
    
    # Variável definida automaticamente
    status: str = __variavel_status # Varia entre "Em aberto", "Em progresso", "Concluído"
    

def atualizacao_status(registro: Manutencao):

    '''
    Função para atualizar os status dos registros após eventuais atualizações de registros.

    parâmetros:

    registro : Variável do tipo Manutencao que recebe o registro que precisa ser atualizado.
    '''

    if registro.data_hora_fim_manutencao == None and registro.data_hora_inicio_manutencao == None:  # Se inicio e fim forem igual a "None", o status recebe "Pendente"
        registro.status = 'Pendente'

    elif registro.data_hora_fim_manutencao != None:  # Se a variável dh_fim_manutencao for diferente de None, status recebe "Concluído"
        registro.status = 'Concluído'

    elif registro.data_hora_inicio_manutencao != None:  # Se a variável dh_inicio_manutencao for diferente de "None", status recebe "Em progresso"
        registro.status = 'Em progresso'

def atualizacao_arm_veiculos_manutencao(arm_veiculos_manutencao: List[dict], lista_manutencoes: List[Manutencao]):

    '''
    Função para atualizar lista de veículos em manutenção.

    parâmetros:

    arm_veiculos_manutencao : Lista de veículos em manutenção que será atualizada.
    lista_manutencoes : Lista usada para fazer a atualização.
    '''

    veiculos_manutencoes_em_progresso = []
    for registro in lista_manutencoes:  # Para cada registro em lista manutencoes

        if registro.status == 'Em progresso':  # Se o status do registro for igual a "Em progresso"
            
            veiculos_manutencoes_em_progresso.append(registro.veiculo)  # Adicionar veículo do registro à lista de manutenções em progresso
            print(registro.veiculo, registro.status, '\n', veiculos_manutencoes_em_progresso)

    arm_veiculos_manutencao[:] = veiculos_manutencoes_em_progresso[:] # Retorna lista de veículos em manutenção em progresso


# Padrão de organização: variáveis contendo prefixo "arm" são usadas para armazenar os dados
arm_manutencoes: List[Manutencao] = []  # Lista que armazenará objetos do tipo "Manutencao" e inicializando lista vazia
arm_veiculos_em_manutencao: List[dict] = []  # Lista que armazenará objetos do tipo "Veiculo" e inicializando lista vazia


# Métodos GET
# /get_manutencao  :  Obtém os registros de manutenções agendadas.
# /get_veiculos_em_manutencao  :  Obtém os veículos onde o status da manutenção é "Em progresso"

@app.get('/')  # Diretório root (home)
def home():
    return {'message': 'Executado com sucesso. Insira uma rota.'}


@app.get('/get_manutencao')
def get_manutencao(request: Request):
    return arm_manutencoes

@app.get('/get_veiculos_em_manutencao')
def get_veiculos_em_manutencao():
    return arm_veiculos_em_manutencao


# Métodos POST  (Inserção de dados)
# /create_manutencao  : Cria um registro de manutenção
# /create_veiculo  : Cria um registro contendo dados do veículo (placa, cliente (proprietário), etc)

@app.post('/create_manutencao')
async def create_manutencao(request: Request):

    body = json.loads( await request.body() )

    manutencao = Manutencao(
        
        id_manutencao = str(uuid4()),

        data_hora_criacao_registro = datetime.today().strftime( '%d/%m/%Y %H:%M:%S' ),

        nome_mecanico = body['nome_mecanico'],
        nome_cliente = body['nome_cliente'],
        
        problema = body['problema'],

        veiculo = {
            "nome": body['nome_veiculo'],
            "placa": body['placa_veiculo']
        }
    )

    arm_manutencoes.append( manutencao )

    return {'message': 'Operação executada com sucesso.', 'id_manutencao_criada': manutencao.id_manutencao}


# Métodos PUT
# /update_dh_inicio_manutencao  :  Atualiza a data e hora de início da manutenção 
# /update_dh_fim_manutencao  :  Atualiza a data e hora do fim da manutenção
# /update_dh_chegada_veiculo  :  Atualiza a data e hora da chegada do veículo

@app.put('/update_inicio_manutencao')
async def update_inicio_manutencao(request: Request):

    body = json.loads( await request.body() )

    for registro in arm_manutencoes:  # Para cada registro na lista arm_manutencoes

        if registro.id_manutencao == body['id_manutencao']:  # Se o id_manutencao for igual ao id da requisição
            
            registro.data_hora_inicio_manutencao = body['data_hora_inicio_manutencao']  # Atualizar o horário do registro

            atualizacao_status( registro )  # Atualizando o status do registro

            atualizacao_arm_veiculos_manutencao( arm_veiculos_em_manutencao, arm_manutencoes )  # Atualizando veiculos em manutenção

            return {'message': 'Operação executada com sucesso.'}  # Retornando que a operação foi executada com sucesso
        
    return {'message': 'ID não encontrado.'}  # Se o ID não for encontrado, retornar "ID não encontrado."

    


@app.put('/update_fim_manutencao')
async def update_fim_manutencao(request: Request):

    body = json.loads( await request.body() )

    for registro in arm_manutencoes:  # Para cada registro na lista arm_manutencoes

        if registro.id_manutencao == body['id_manutencao']:  # Se o id do registro for igual ao id da requisição

            registro.data_hora_fim_manutencao = body['data_hora_fim_manutencao']  # Atualizar o horário do registro

            atualizacao_status( registro )  # Atualizando o status do registro

            atualizacao_arm_veiculos_manutencao( arm_veiculos_em_manutencao, arm_manutencoes )  # Atualizando veiculos em manutenção
            
            return {'message': 'Operação executada com sucesso.'}  # Retornando que a operação foi executada com sucesso
        
    return {'message': 'ID não encontrado.'}  # Se o ID não for encontrado, retornar "ID não encontrado."
    

@app.put('/update_chegada_veiculo')
async def update_dh_chegada_veiculo(request: Request):

    body = json.loads( await request.body() )

    for registro in arm_manutencoes:  # Para cada registro na lista arm_manutencoes

        if registro.id_manutencao == body['id_manutencao']:  # Se o id do registro for igual ao id da requisição

            registro.data_hora_chegada_veiculo = body['data_hora_chegada_veiculo']  # Atualizar o horário do registro

            atualizacao_status( registro )  # Atualizando o status do registro

            return {'message': 'Operação executada com sucesso.'}  # Retornando que a operação foi executada com sucesso
        
    return {'message': 'ID não encontrado.'}  # Se o id não for encontrado, retornar "ID não encontrado."
    

# Métodos DELETE
# /delete_manutencao  : Deleta um registro de manutenção.

@app.delete('/delete_manutencao')
async def delete_manutencao(request: Request):

    body = json.loads( await request.body() )

    for registro in arm_manutencoes:  # Para cada registro na lista arm_manutencoes
        
        if registro.id_manutencao == body['id_manutencao']:  # Se o id do registro for igual ao id da requisição
        
            if registro.status not in 'Concluído':  # Se o status não for "Concluído"

                arm_manutencoes.remove( registro )  # Então remover o registro da lista arm_manutencoes

                atualizacao_arm_veiculos_manutencao(arm_veiculos_em_manutencao, arm_manutencoes)  # Atualizando veiculos em manutenção

                return {'message': 'Operação executada com sucesso.'}  # Retornando que a operação foi executada
            
            # Se o status for "Concluído", retornar que não foi possível executar operação
            return {'message': f'Operação não pôde ser executada. Status da manutenção: {registro.status}'}
        
    return {'message': 'ID não encontrado.'}  # Se o ID não for encontrado, retornar "ID não encontrado."