from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Optional
import secrets
import os

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

import asyncio

from dotenv import load_dotenv
load_dotenv()



DATABASE_URL = os.getenv("DATABASE_URL")

DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI(
    title="API de livros",
    description="API para gerenciar livros",
    version="1.0.0",
    contact={
        "nome":"Gustavo",
        "Email":"Gustavopellegrinofialho25@gmail.com"
    }
)

MEU_USUARIO = os.getenv("MEU_USUARIO")
MINHA_SENHA = os.getenv("MINHA_SENHA")

security = HTTPBasic()


class LivroDB(Base):
    __tablename__ = "Livros"
    id = Column(Integer, primary_key=True, index=True)
    nome_livro = Column(String, index=True)
    autor_livro = Column(String, index=True)
    ano_livro = Column(Integer)
    
class Livro(BaseModel):
       nome_livro: str
       autor_livro: str
       ano_livro: int
    
Base.metadata.create_all(bind=engine)

def sessao_db():
   db = SessionLocal()
   try:
      yield db
   finally:
      db.close()
    
def autenticar_meu_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    
    is_username_correct = secrets.compare_digest(credentials.username,MEU_USUARIO)
    is_password_correct = secrets.compare_digest(credentials.password,MINHA_SENHA)
    
    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=401,
            detail="Usuario ou senha incorretos",
            headers={"WWW-Authenticate": "Basic"}
        )
    

@app.get("/")
async def Hello_world():
    return {"message": "Hello guys"}

async def chamadas_externas_1():
    await asyncio.sleep(2)
    return "Resultado chamada externa 1"

async def chamadas_externas_2():
    await asyncio.sleep(2)
    return "Resultado chamada externa 2"

async def chamadas_externas_3():
    await asyncio.sleep(2)
    return "Resultado chamada externa 3"

@app.get("/chamadas-externas")
async def chamadas_externas():
    tarefa1 = asyncio.create_task(chamadas_externas_1())
    tarefa2 = asyncio.create_task(chamadas_externas_2())
    tarefa3 = asyncio.create_task(chamadas_externas_3())
    
    resultado1 = await tarefa1
    resultado2 = await tarefa2
    resultado3 = await tarefa3
    
    return {
        "message": "Todos as chamadas nos API's foram concluidas com sucesso",
        "resultado": [resultado1, resultado2, resultado3]
    }

@app.get("/livros")
async def get_livros(page: int = 1, limit: int = 10, db: Session = Depends(sessao_db) , credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    if page < 1 or limit < 1:
      raise HTTPException(status_code=400, detail="Page ou limit estao com valores invalidos")
    
    livros = db.query(LivroDB).offset((page - 1) * limit).limit(limit).all()
    
    if not livros:
     return {"message": "Nao existe nenhum livro"}
     
    
    total_livros = db.query(LivroDB).count()

    return {
        "page": page,
        "limit": limit,
        "total": total_livros, 
        "livros": [{"id": livro.id, "nome_livro": livro.nome_livro, "autor_livro": livro.autor_livro, "ano_livro": livro.ano_livro} for livro in livros]
    }
    
    
@app.post("/adiciona")
async def post_livros(livro: Livro, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    db_livro = db.query(LivroDB).filter(LivroDB.nome_livro == livro.nome_livro, LivroDB.autor_livro == livro.autor_livro).first()
    if db_livro:
        raise HTTPException(status_code=400, detail="Esse livro ja existe no banco de dados")
     
    novo_livro = LivroDB(nome_livro=livro.nome_livro, autor_livro=livro.autor_livro, ano_livro=livro.ano_livro)
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)
    
    return {"Message": "O livro foi criado com sucesso"}
     

@app.put("/atualiza/{id_livro}")
async def put_livros(id_livro: int, livro: Livro, db: Session = Depends(sessao_db),credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
   db_livro = db.query(LivroDB).filter(LivroDB.id == id_livro).first()
   if not db_livro:
      raise HTTPException(status_code=404, detail="Esse livro nao foi encontrado no seu banco de dados")
   
   db_livro.nome_livro = livro.nome_livro
   db_livro.autor_livro = livro.autor_livro
   db_livro.ano_livro = livro.ano_livro
   
   db.commit()
   db.refresh(db_livro)
   
   return {"message": "seu livro foi atualizado com sucesso"}
    


@app.delete("/deletar/{id_livro}")
async def delete_livro(id_livro: int, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    db_livro = db.query(LivroDB).filter(LivroDB.id == id_livro).first()
    
    if not db_livro:
       raise HTTPException(status_code=404, detail="Esse livro nao existe no seu banco de dados")
    
    db.delete(db_livro)
    db.commit()
    
    return {"Message": "Seu livro foi deletado com sucesso"}