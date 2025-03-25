insert into clientes values (1, 'BrazilHealth', '211758244095336');
insert into clientes values (2, 'Aquila Aceleradora', '503815775365718');
insert into clientes values (3, 'Enaya Branding', '402318552878343');


CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    meta_account_id VARCHAR(50) UNIQUE -- ID da conta do cliente no Meta Ads
);

CREATE TABLE meta_ads_data (
    id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES clientes(id) ON DELETE CASCADE, -- Referência ao cliente
    data_inicio DATE NOT NULL, -- Período da consulta (início)
    data_fim DATE NOT NULL, -- Período da consulta (fim)
    impressions INT NOT NULL, 
    clicks INT NOT NULL,
    ctr NUMERIC(10, 6) NOT NULL,
    cpc NUMERIC(10, 6) NOT NULL,
    cpm NUMERIC(10, 6) NOT NULL,
    spend NUMERIC(10, 2) NOT NULL,
    leads INT NOT NULL,
    cpl NUMERIC(10, 2) NOT NULL
);

select * from meta_ads_data

UPDATE clientes
SET meta_account_id = '211758244095336'
WHERE id = 1;
 