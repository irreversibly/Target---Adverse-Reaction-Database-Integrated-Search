import pandas as pd
import sys

def cleaner(drug_file, legacy_reac, current_reac):	
	
	drug = pd.read_csv(drug_file, dtype=object)
	side_effect_legacy = pd.read_csv(legacy_reac, dtype=object)
	side_effect_current = pd.read_csv(current_reac, dtype=object)

	drug_pt_1 = pd.merge(drug[['primaryid','isr','lookup_value']], side_effect_legacy, how='left', on='isr')
	drug_pt_2 = pd.merge(drug_pt_1, side_effect_current, how='left', on='primaryid')
	drug_pt_2['reac_pt_list'] = drug_pt_2['reac_pt_list_x'].fillna(drug_pt_2['reac_pt_list_y'])

	drug_all = drug_pt_2.drop(columns=['reac_pt_list_x', 'reac_pt_list_y'])
	drug_all_no_pt_na = drug_all.dropna(subset=['reac_pt_list'])
	drug_all_no_pt_na['reac_pt_list'] = drug_all_no_pt_na['reac_pt_list'].apply(lambda x: x.split('|'))
	drug_all_no_pt_na.to_csv('faers_data_with_codes', sep='\t', index=False)

	faers_pairwise = drug_all_no_pt_na[['lookup_value', 'reac_pt_list']].explode('reac_pt_list')
	faers_pairwise['reac_pt_list'] = faers_pairwise['reac_pt_list'].str.lower()
	faers_pairwise.to_csv('faers_pairwise.input', sep='\t', index=False)

if __name__ == "__main__":
	drug_file = sys.argv[1]
	legacy_reac = sys.argv[2]
	current_reac = sys.argv[3]
	cleaner(drug_file, legacy_reac, current_reac)

