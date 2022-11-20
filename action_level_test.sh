mkdir -p action_level_results/
for ACTION in bi_enc tfm_ner use_enc use_qa ent_ext text_seg cl_summer
do
	jsctl -f local.session jsorc loadtest -test action_level_test -experiment $ACTION -o action_level_results/$ACTION.json
	jsctl -f local.session jsorc restart django
	sleep 15
done
