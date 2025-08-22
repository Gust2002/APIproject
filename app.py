from fastapi import FastAPI, HTTPException, status

app = FastAPI()

meus_livrozinhos = {}

class Livros():
    nome_livro = str
    autor_livro = str
    ano_livro = str 

@app.get("/")
def hello_world():
    return {"Message": "Hello guys"}

@app.get("/adiciona")
def get_livros():
    if not meus_livrozinhos:
        return {"Message": "Nao existe nenhum livro"}
    else:
        return {"Livros": meus_livrozinhos}

@app.post("/adicona")
def post_livro(id_livro: int, livro: Livros):
    if id_livro in meus_livrozinhos:
        raise HTTPException(status_code=400,detail="Esse livro ja existe parceiro")
    else:
        meus_livrozinhos[id_livro] = livro.dict()
        
        return {"Message": "Seu livro foi criado com sucesso!"}

@app.put("/atualizar/{id_livro}")
def put_livros(id_livro: int, livro: Livros):
 livro = meus_livrozinhos.get(id_livro)
 if not livro:
     raise HTTPException(status_code=404,detail="Esse livro nao foi encontrado")
 else:
     meus_livrozinhos[id_livro] = livro.dict()
     return {"Message": "Seu livro foi atualizado com sucesso"}
 
@app.delete("deletar/{id_livro}")
def deleta_livro(id_livro, int):
    if id_livro not in meus_livrozinhos:
        raise HTTPException(status_code=500,detail="Esse livro nao foi encontrado amigao")
    else:
        del meus_livrozinhos[id_livro]
        return {"Message": "Seu livro foi deletadop com sucesso"}
 
 
    
