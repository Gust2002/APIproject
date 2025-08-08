## API de livros 

# GT, POST, PUT, DELETE 

# POST- Adicionar novos livros (Create)
# GET - Buscar os dados dos livros (Read)
# PUT - Atualizar informacoes dos livros (Update)
# DELETE - Deletar informacoes dos livroa (Delete)
#Create
#Read
#Update
#Delete

# Vamos acessar nosso Endpoint
# E vamos acessar os PTH'S desse

# path ou rota
# query strings 

# 200 300 400 500

# Fabrica -> Lojista -> Consumidor

# Documentacao swagger -> Documentar os endpoints da nossa aplicacao (do nossa API)


from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Optional
import secrets
import os

app = FastAPI(
   title ="API de livros",
   description="API para gerenciar livros.",
   version="1.0.2.0",
contact={
   "nome":"Gustavo",
   "email":"Gustavopellegrinofialho25@gmail.com"
      
   }
)

MEU_USUARIO = "admin"
MINHA_SENHA = "admin"

security = HTTPBasic()

meus_livrozinhos = {}

class Livro(BaseModel):
   nome_livro: str
   autor_livro: str
   ano_livro: int

def autenticar_meu_usuario(credentials: HTTPBasicCredentials = Depends(security)):
   is_username_correct = secrets.compare_digest(credentials.username.encode, MEU_USUARIO)
   is_password_correct = secrets.compare_digest(credentials.username, MINHA_SENHA)

   if not (is_username_correct and is_password_correct):
      raise HTTPBasic(
         status_code=401,
         detail="Usuario ou senha incorretos",
         headers={"WWW-Authentication": "Basic"}
         
      )
   
@app.get("/")
def hello_world():
   return {"Hello": "World"}


@app.get("/livros")
def get_livros(page: int = 1, limit: int = 10):
   if page < 1 or limit < 1:
      raise HTTPException(status_code=400, detail="Pagina nao encontrada!!")
   
   if not  meus_livrozinhos:
      return {"Message:" "Nao existe nenhum livro"}
   
   start = (page - 1) * limit
   end =  start + limit

   livros_paginados = [
      {"id": id_livro, "nome_livro": livro_data["nome_livro"], "autor_livro": livro_data["autor_livro"], "ano_livro": livro_data["ano_livro"]}
      for id_livro, livro_data in list(meus_livrozinhos.items())[start:end]
   ]
   
   return{
       "page": page,
       "limit": limit,
       "total": len(meus_livrozinhos),
       "livros": livros_paginados
    }


# Id_livro
# Nome do livro
# Autor do livro 
# ano do lancamento do livro

@app.post("/adiciona")
def post_livros(id_livro: int, livro: Livro):
    if id_livro in meus_livrozinhos:
        raise HTTPException(status_code=400, detail="esse livro ja existe, meu parceiro")
    else:
        meus_livrozinhos[id_livro] = livro.dict()
        return {"message":"o livro foi criado com sucesso"}
    


# fabrica -> tenis que precisa ser mudada a cor! 
#1. quem e o tenis -> livro -> id_livro
#2. pegar o tenis -> pega o livro -> id_livro 
#3. processo de pintura para mudar a cor -> atualizacao das informacoes do livro


@app.put("/atualiza/{id_livro}")
def put_livros(id_livro: int, livro: Livro):
    meu_livro = meus_livrozinhos.get(id_livro)
    if not meu_livro:
        raise HTTPException(status_code=404, detail="esse livro nao foi encontrado!")
    else:
        meus_livrozinhos[id_livro] = livro.dict()
        return {"message": "As informacoes do seu livro foram atualizadas"}


@app.delete("/deletar/{id_livro}")
def delete_livro(id_livro: int):
 if id_livro not in meus_livrozinhos:
  raise HTTPException(status_code=404, detail="esse livro nao foi encontrado")
 else:
  del meus_livrozinhos[id_livro]
 return {"message": "seu livro foi encontrado com sucesso!"}