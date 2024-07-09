select 
    case 
		when te.CLASSIFICATION_STR = 'HYDROLASE' then 0
        when te.CLASSIFICATION_STR = 'TRANSFERASE' then 1
        when te.CLASSIFICATION_STR = 'OXIDOREDUCTASE' then 2
        when te.CLASSIFICATION_STR = 'LYASE' then 3
	END as y,
    seq.SEQUENCE_STR as sequencia
from protein_data_bank.tipo_estrutura te
inner join protein_data_bank.sequencia_estrutura seq
	on seq.STRUCTUREID_STR = te.STRUCTUREID_STR
where
    te.CLASSIFICATION_STR in ('HYDROLASE', 'TRANSFERASE', 'OXIDOREDUCTASE', 'LYASE')