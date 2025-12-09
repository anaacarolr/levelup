from datetime import datetime

from flask import Flask, render_template, redirect, url_for, request, flash
from sqlalchemy.exc import SQLAlchemyError

from models import local_session, Jogos, Categoria, Usuario, Favorito
from sqlalchemy import select, desc, func

app= Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'PlayFuture'
app.config['SECRET_KEY'] = 'senha'

@app.route('/')
def index():
    return redirect(url_for('get_jogos'))

@app.route('/jogos')
def get_jogos():
    db_session = local_session()
    try:

        sql_jogos = select(Jogos)
        resultado = db_session.execute(sql_jogos).scalars().all()
        print(resultado)
        return render_template('home.html', jogos=resultado)
    except SQLAlchemyError as e:
        print(f'Erro na base de dados: {e}')
        return redirect(url_for('index'))
    except Exception as ex:
        print(f'Ocorreu um erro ao consultar os jogos: {ex}')
        return redirect(url_for('index'))
    finally:
        db_session.close()

@app.route('/criar_game', methods=['GET','POST'])
def post_jogos():
    db_session = local_session()

    if request.method == 'POST':
        if not request.form['form_nome']:
            flash("Preencha o titulo/nome do jogo", "error")
            return redirect(url_for('post_jogos'))
        if not request.form['form_categoria']:
            flash("Preencha a categoria do jogo", "error")
            return redirect(url_for('post_jogos'))
        else:
            dados_jogos = Jogos(
                nome_jogo=request.form['form_nome'],
                descricao_jogo=request.form['form_descricao'],
                data_de_criacao=datetime.strptime(request.form['form_data'], '%Y-%m-%d'),
                n_players=int(request.form['form_players']),
                jogo_free_ou_pago=request.form['form_jogo_free_ou_pago'],
                clasificacao=request.form['form_clasificacao'],
                url_img=request.form['form_url_img'],
                categoria =int(request.form['form_categoria'])
            )
        try:

            db_session.add(dados_jogos)
            db_session.commit()
            flash("Jogo criado com sucesso!", "success")
            return redirect(url_for('post_jogos'))
        except SQLAlchemyError as e:
            print(f'Erro no banco ao cadastrar jogos: {e}')
            db_session.rollback()
        except Exception as ex:
            print(f'Erro ao cadastrar jogos: {ex}')
            db_session.rollback()
        finally:
            db_session.close()
    sql_categoria = select(Categoria)
    resultado = db_session.execute(sql_categoria).scalars().all()

    return render_template('formulariojogos.html', categorias=resultado)

@app.route('/categoria')
def get_categoria():
    db_session = local_session()
    try:
        sql_categoria = select(Categoria)
        resultado = db_session.execute(sql_categoria).scalars().all()
        print(resultado)
        return render_template('categoria.html', categorias=resultado)
    except SQLAlchemyError as e:
        print(f'Erro na base de dados: {e}')
    except Exception as ex:
        print(f'Ocorreu um erro ao consultar as categorias: {ex}')
    finally:
        db_session.close()


@app.route('/criar_categoria', methods=['GET','POST'])
def post_categoria():
    if request.method == 'POST':
        if not request.form['form_nome_categoria']:
            flash("Preencha o nome da categoria", "error")
        else:
            dados_categoria = Categoria(nome=request.form['form_nome_categoria'])
        db_session = local_session()
        try:
            db_session.add(dados_categoria)
            db_session.commit()
            flash("categoria criada com sucesso!", "success")
            return redirect(url_for('post_categoria'))
        except SQLAlchemyError as e:
            print(f'Erro no banco ao cadastrar categoria: {e}')
            db_session.rollback()
        except Exception as ex:
            print(f'Erro ao cadastrar categoria: {ex}')
            db_session.rollback()
        finally:
            db_session.close()
    return render_template('formulario_categoria.html')

@app.route('/ver_jogo/<int:jogo_id>')
def get_ver_jogo(jogo_id):
    db_session = local_session()
    try:
        sql_ver = (select(Jogos,Categoria)
                   .join(Categoria, Categoria.id == Jogos.categoria)
                   .where(Jogos.id == jogo_id ))
        resultado = db_session.execute(sql_ver).all()
        print('ddf',resultado)
        return render_template('ver_jogo.html', ver_jogo=resultado)
    except SQLAlchemyError as e:
        print(f'Erro na base de dados: {e}')
        return redirect(url_for('index'))
    except Exception as ex:
        print(f'Ocorreu um erro ao consultar os jogos: {ex}')
        return redirect(url_for('index'))
    finally:
        db_session.close()

@app.route('/criar_pessoa', methods=['GET','POST'])
def post_usuario():
    if request.method == 'POST':
        if not request.form['form_nome_usuario']:
            flash("Preencha o nome do seu usuario", "error")
        else:
            dados_usuario = Usuario(nome_usuario=request.form['form_nome_usuario'],
                                    data_de_nascimento=request.form["form_data_de_nascimento"],
                                    senha=request.form['form_senha'])
        db_session = local_session()
        try:
            db_session.add(dados_usuario)
            db_session.commit()
            flash("usuario criado com sucesso!", "success")
            return redirect(url_for('index'))
        except SQLAlchemyError as e:
            print(f'Erro no banco ao cadastrar usuario: {e}')
            db_session.rollback()
            return redirect(url_for('index'))
        except Exception as ex:
            print(f'Erro ao cadastrar usuario: {ex}')
            db_session.rollback()
            return redirect(url_for('index'))
        finally:
            db_session.close()
    return render_template('formulario_pessoa.html')


@app.route('/ranking')
def lista_ranking():
    db_session = local_session()
    try:
        sql_lista_ranking = (
            select(Jogos)
            .order_by(desc(Jogos.n_players))  # agora ordena do maior para o menor
            .limit(10)
        )
        resultado = db_session.execute(sql_lista_ranking).scalars().all()
        print('ddd', resultado)
        return render_template('lista_ranking.html', jogos=resultado)

    except SQLAlchemyError as e:
        print(f'Erro na base de dados: {e}')
    except Exception as ex:
        print(f'Ocorreu um erro ao consultar o Ranking: {ex}')
    finally:
        db_session.close()


if __name__ == '__main__':
    app.run(debug=True)
