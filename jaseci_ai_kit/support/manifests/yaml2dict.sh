for MODULE in cl_summer tfm_ner bi_enc fast_enc pdf_ext ent_ext text_seg use_enc use_qa;
do
	if [ $MODULE = use_enc ] || [ $MODULE = use_qa ]
	then
		kubectl-convert -f prod/$MODULE.yaml --local -o json > temp.json
	else
		kubectl-convert -f $MODULE.yaml --local -o json > temp.json
	fi
	python gen_dict.py $MODULE > ${MODULE}_action_config.py
done
rm temp.json