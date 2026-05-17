CREATE DATABASE IF NOT EXISTS loja_virtual
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE loja_virtual;
 
CREATE TABLE categorias (
  id          INT PRIMARY KEY,
  nome        VARCHAR(50)  NOT NULL,
  descricao   VARCHAR(200)
);
 
CREATE TABLE clientes (
  id            INT PRIMARY KEY,
  nome          VARCHAR(100) NOT NULL,
  email         VARCHAR(100) UNIQUE,
  cidade        VARCHAR(50),
  estado        VARCHAR(2),
  data_cadastro DATE,
  ativo         BOOLEAN DEFAULT TRUE
);
 
CREATE TABLE produtos (
  id            INT PRIMARY KEY,
  nome          VARCHAR(100) NOT NULL,
  preco         DECIMAL(10,2) NOT NULL,
  categoria_id  INT,
  estoque       INT DEFAULT 0,
  FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);
 
CREATE TABLE pedidos (
  id          INT PRIMARY KEY,
  cliente_id  INT,
  data_pedido DATE,
  status      VARCHAR(20),
  total       DECIMAL(12,2),
  FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);
 
CREATE TABLE itens_pedido (
  id             INT PRIMARY KEY,
  pedido_id      INT,
  produto_id     INT,
  quantidade     INT,
  preco_unitario DECIMAL(10,2),
  FOREIGN KEY (pedido_id)  REFERENCES pedidos(id),
  FOREIGN KEY (produto_id) REFERENCES produtos(id)
);