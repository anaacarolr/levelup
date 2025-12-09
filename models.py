#importar bibliotecas
from sqlalchemy import create_engine, Column, DateTime, func, ForeignKey, Integer, String, Enum, Text
from sqlalchemy.orm import sessionmaker, declarative_base

#criar conexao com a base de dados
engine = create_engine('mysql+mysqlconnector://root:senaisp@localhost:3306/levelup')

#configurar seções locais
local_session = sessionmaker(bind=engine)
base = declarative_base()

class Jogos(base):
    __tablename__ = 'jogos'
    id = Column(Integer, primary_key=True)
    descricao_jogo = Column(String(60), nullable=False)
    data_de_criacao = Column(DateTime, nullable=False)
    n_players = Column(Integer, nullable=False)
    nome_jogo = Column(String(60), nullable=False)
    jogo_free_ou_pago = Column(Enum("free", "pago"), nullable=False)
    clasificacao = Column(Enum("Livre","10","12","14","16","18"), nullable=False)
    url_img = Column(Text, nullable=False)
    categoria = Column(Integer, ForeignKey('categoria.id'))

    def __repr__(self):
        return f'<Usuario(descricao_jogo={self.descricao_jogo}, data_de_criacao={self.data_de_criacao}, n_players={self.n_players}, nome_jogo={self.nome_jogo}, clasificacao={self.clasificacao}, url_img={self.url_img}, categoria={self.categoria})>)'


class Categoria(base):
    __tablename__ = 'categoria'
    id = Column(Integer, primary_key=True)
    nome = Column(String(60), nullable=False)

    def __repr__(self):
        return f'<Categoria(nome={self.nome})>'

class Usuario(base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True)
    nome_usuario = Column(String(60), nullable=False)
    data_de_nascimento = Column(DateTime, nullable=False)
    email = Column(String(100), nullable=False)
    senha = Column(String(100), nullable=False)

    def __repr__(self):
        return f'<Pessoa(nome_pessoa={self.nome_usuario}, data_de_nascimento={self.data_de_nascimento}, email={self.email}, senha={self.senha})>'

class Favorito(base):
    __tablename__ = "favoritos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_fk_usuario = Column(Integer, ForeignKey("usuario.id"))
    id_fk_jogo = Column(Integer, ForeignKey("jogos.id"))

    def __repr__(self):
        return f'<Favorito(id={self.id})>'

