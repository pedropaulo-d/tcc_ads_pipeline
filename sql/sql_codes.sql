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
    cliente_id INTEGER REFERENCES clientes(id),
    data_inicio DATE,
    data_fim DATE,
	campaign_id TEXT,  -- ID da campanha (se for geral, pode ser NULL)
    campaign_name TEXT,  -- Nome da campanha
    impressions INTEGER,
    clicks INTEGER,
    ctr FLOAT,
    cpc FLOAT,
    cpm FLOAT,
    spend FLOAT,
    leads INTEGER,
    cpl FLOAT
);

select * from meta_ads_data
select * from clientes

select t1.nome, t2.data_inicio, t2.data_fim, t2.campaign_name
from clientes as t1
inner join meta_ads_data as t2
on t1.id = t2.cliente_id

select * from meta_ads_data

UPDATE clientes
SET meta_account_id = '211758244095336'
WHERE id = 1;
 