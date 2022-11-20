mkdir -p synthetic_apps_results/
for APP in sentence_pairing discussion_analysis zeroshot_faq_bot flight_chatbot restaurant_chatbot flow_analysis virtual_assistant
do
	for MEM in 4 6 8
	do
		echo "RUNNING $APP $MEM"
		jsctl -f local.session jsorc loadtest -test synthetic_apps -experiment $APP -mem $MEM -o synthetic_apps_results/$APP-$MEM.json
		sleep 10
		jsctl -f local.session jsorc restart django
		sleep 30
	done
done
