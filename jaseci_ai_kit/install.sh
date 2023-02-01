#!/bin/bash

JAC_NLP_MODULES=("bart_sum" "cl_summer" "ent_ext" "fast_enc" "sbert_sim" "t5_sum" "text_seg" "tfm_ner" "use_enc" "use_qa" "zs_classifier" "bi_enc" "topic_ext")
JAC_SPEECH_MODULES=("stt" "tts", "vc_tts")
JAC_MISC_MODULES=("pdf_ext" "translator" "cluster" "ph")
JAC_VISION_MODULES=("detr" "rftm" "yolos" "dpt")

install_modules() {
	if [[ $1 == "all" ]]; then
		echo -e "\033[0;32mInstalling all the modules\033[0m"
		cd jac_speech
		pip install -e .[all]
		cd ../jac_nlp
		pip install -e .[all]
		cd ../jac_misc
		pip install -e .[all]
		cd ../jac_vision
		pip install -e .[all]
		return
	fi

	modules=("$@")
	for module in "${modules[@]}"; do
		echo -e "\033[0;32mInstalling ${module}\033[0m"
		if [[ " ${JAC_NLP_MODULES[@]} " =~ " ${module} " ]]; then
			cd jac_nlp
			pip install -e .[${module}]
			cd ..
		elif [[ " ${JAC_SPEECH_MODULES[@]} " =~ " ${module} " ]]; then
			cd jac_speech
			pip install -e .[${module}]
			cd ..
		elif [[ " ${JAC_MISC_MODULES[@]} " =~ " ${module} " ]]; then
			cd jac_misc
			pip install -e .[${module}]
			cd ..
		elif [[ " ${JAC_VISION_MODULES[@]} " =~ " ${module} " ]]; then
			cd jac_vision
			pip install -e .[${module}]
			cd ..
		else
			# add color to  echo "Invalid module: ${module}"
			echo -e "\033[0;31mInvalid module: ${module}\033[0m"
		fi
	done
}

install_modules "$@"