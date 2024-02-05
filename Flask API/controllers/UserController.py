from flask import Response, request
from models.User import User
from flask_sqlalchemy import SQLAlchemy
import json
from models.User import db

def index():
    session = db.session()
    users = session.query(User).all()
    users_json = [user.serialize() for user in users]
    session.close()
    return Response(json.dumps(users_json))

def store():
    body = request.get_json()
    session = db.session()
    try:
        user = User(name=body['name'],telefone=body['telefone'],address=body['address'],CPF=body['CPF'])
        session.add(user)
        session.commit()
        return Response(json.dumps([user.serialize()]))
    except Exception as e:
        session.rollback()
        return {"Erro":"Não conseguimos gravar o usuário!"}
    finally:
        session.close()

def show(user_id):
    session = db.session()
    try:
        user = session.query(User).get(user_id)
        return Response(json.dumps([user.serialize()]))
    except Exception as e:
        session.rollback()
        return {"Erro":"Não conseguimos retornar o usuário!"}
    finally:
        session.close()

def update(user_id):
    session = db.session()
    try:
        body = request.get_json()
        user = session.query(User).get(user_id)

        if body and body['name']:
            user.name = body['name']
        if body and body['telefone']:
            user.age = body['telefone']
        if body and body['address']:
            user.address = body['address']
        if body and body['CPF']:
            user.address = body['CPF']
        session.commit()

        return Response(json.dumps([user.serialize()]))
    except Exception as e:
        session.rollback()
        return {"Erro":"Não conseguimos atualizar o usuário!"}
    finally:
        session.close()

def destroy(user_id):
    session = db.session()
    try:
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return {"ok":"Usuário foi Excluído com sucesso!"}
    except Exception as e:
        session.rollback()
        return {"Erro":"Não conseguimos retornar o usuário!"}
    finally:
        session.close()