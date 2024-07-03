select 
    te.CLASSIFICATION_STR as y,
    inf.CRYSTALLIZATIONTEMPK_FLOAT as temperatura_cristalizacao_k,
    inf.RESIDUECOUNT_INT as contagem_residuos,
    inf.RESOLUTION_FLOAT as medida_de_resolucao,
    inf.STRUCTUREMOLECULARWEIGHT_FLOAT as peso_molecular,
    va.PHVALUE_FLOAT as ph,
    va.DENSITYPERCENTSOL_FLOAT as densidade_percentual_solucao
from protein_data_bank.tipo_estrutura te
inner join protein_data_bank.infos_estrutura inf
	on inf.STRUCTUREID_STR = te.STRUCTUREID_STR
inner join protein_data_bank.valores_analiticos va
	on va.STRUCTUREID_STR = te.STRUCTUREID_STR
where
    te.CLASSIFICATION_STR in ('HYDROLASE', 'TRANSFERASE', 'OXIDOREDUCTASE', 'LYASE')