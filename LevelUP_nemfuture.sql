create database levelUP;
use levelUP;

-- DCL
/* segurança
criar usuario
configurar Grant(privilegios)
root - admin
*/

create table if not exists usuario (
	id int auto_increment primary key,
    nome_usuario varchar(60),
    data_de_nascimento date,
    email varchar(100) unique not null 
);

create table if not exists jogos (
	id int auto_increment primary key,
    descricao_jogo varchar(60),
    data_de_criacao date,
    n_players int,
    nome_jogo varchar(60),
    jogo_free_ou_pago ENUM('free','pago') default 'free'
);

create table if not exists categoria (
	id int auto_increment primary key,
    nome varchar(60)
);

create table if not exists empresa (
	id int auto_increment primary key,
    descricao_empresa varchar(60)
);

create table if not exists plano_de_pagamento (
	id int auto_increment primary key,
    forma_de_pagamento ENUM('cartao credito','cartao debito','pix') default 'pix',
    preco numeric
);

create table if not exists favorito (
	id int auto_increment primary key
);

drop table plano_de_pagamento;

-- alter table funcionario add sexo varchar(10); -- adicionar coluna
-- alter table funcionario rename column nome to nome_funcionario; -- trocar nome da coluna

