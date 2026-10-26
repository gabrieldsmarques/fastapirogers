from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Tarefa(BaseModel):
    titulo: str
    desc: str
    concluida: bool = False

class TarefaSaida(Tarefa):
    id: int

tarefas = {}

@app.get("/tarefas", response_model=list[TarefaSaida])
async def listar_tarefas():
    return list(tarefas.values())

@app.post("/tarefas")
async def criar_tarefa(tarefa: Tarefa):
    novo_id = len(tarefas) + 1
    saida = TarefaSaida(id=novo_id, titulo=tarefa.titulo, desc=tarefa.desc, concluida=tarefa.concluida)
    tarefas[novo_id] = saida
    return saida

@app.get("/tarefas/{tarefa_id}", response_model=TarefaSaida)
async def buscar_tarefa(tarefa_id: int):
    if tarefa_id not in tarefas:
        raise HTTPException(status_code=404, detail="essa tarefa não existe")
    return tarefas[tarefa_id]

@app.put("/tarefas/{tarefa_id}", response_model=TarefaSaida)
async def atualizar_tarefa(tarefa_id: int, tarefa: Tarefa):
    if tarefa_id not in tarefas:
        raise HTTPException(status_code=404, detail="essa tarefa não existe")
    saida = TarefaSaida(id=tarefa_id, titulo=tarefa.titulo, desc=tarefa.desc, concluida=tarefa.concluida)
    tarefas[tarefa_id] = saida
    return saida

@app.delete("/tarefas/{tarefa_id}")
async def apagar_tarefa(tarefa_id: int):
    if tarefa_id not in tarefas:
        raise HTTPException(status_code=404, detail="essa tarefa não existe")
    del tarefas[tarefa_id]
    return {"mensagem": "tarefa apagada"}