# flake8: noqa
test_entity_detection_request = {
    "text": "The Humboldt University of Berlin is situated in Berlin, Germany",
    "ner_labels": ["PREDEFINED"],
}

test_entity_detection_valid_req = {
    "text": "what does Settlement means?",
    "ner_labels": ["Fin_Corp", "LOC", "ORG"],
}
test_entity_detection_valid = {
    "entities": [
        {
            "entity_text": "Settlement",
            "entity_value": "Fin_Corp",
            "conf_score": 0.9134525060653687,
            "start_pos": 10,
            "end_pos": 20,
        }
    ]
}
test_entity_detection_response = {
    "entities": [
        {
            "entity_text": "Humboldt University of Berlin",
            "entity_value": "ORG",
            "conf_score": 0.9708927571773529,
            "start_pos": 4,
            "end_pos": 33,
        },
        {
            "entity_text": "Berlin",
            "entity_value": "LOC",
            "conf_score": 0.9977847933769226,
            "start_pos": 49,
            "end_pos": 55,
        },
        {
            "entity_text": "Germany",
            "entity_value": "LOC",
            "conf_score": 0.9997479319572449,
            "start_pos": 57,
            "end_pos": 64,
        },
    ]
}

test_entity_detection_request_fail_ner = {
    "text": "The Humboldt University of Berlin is situated in Berlin, Germany",
    "ner_labels": [],
}

test_entity_detection_request_fail_text = {
    "text": "",
    "ner_labels": ["City", "Country"],
}


test_entity_training_pass = {
    "train_data": [
        {
            "context": "what does Settlement means?",
            "entities": [
                {
                    "entity_value": "Settlement",
                    "entity_type": "Fin_Corp",
                    "start_index": 10,
                    "end_index": 20,
                }
            ],
        },
        {
            "context": "what does Home-Equity Loan means?",
            "entities": [
                {
                    "entity_value": "Home-Equity Loan",
                    "entity_type": "Fin_Corp",
                    "start_index": 10,
                    "end_index": 26,
                }
            ],
        },
        {
            "context": "what does Closed-Ended Credit stands for?",
            "entities": [
                {
                    "entity_value": "Closed-Ended Credit",
                    "entity_type": "Fin_Corp",
                    "start_index": 10,
                    "end_index": 29,
                }
            ],
        },
        {
            "context": "what does Adjustable-Rate Mortgage stands for?",
            "entities": [
                {
                    "entity_value": "Adjustable-Rate Mortgage",
                    "entity_type": "Fin_Corp",
                    "start_index": 10,
                    "end_index": 34,
                }
            ],
        },
        {
            "context": "what is the full form of Interest Cap ?",
            "entities": [
                {
                    "entity_value": "Interest Cap",
                    "entity_type": "Fin_Corp",
                    "start_index": 25,
                    "end_index": 37,
                }
            ],
        },
        {
            "context": "what is the full form of Title Insurance Policy ?",
            "entities": [
                {
                    "entity_value": "Title Insurance Policy",
                    "entity_type": "Fin_Corp",
                    "start_index": 25,
                    "end_index": 47,
                }
            ],
        },
        {
            "context": "what actually Mortgage Banker is ?",
            "entities": [
                {
                    "entity_value": "Mortgage Banker",
                    "entity_type": "Fin_Corp",
                    "start_index": 14,
                    "end_index": 29,
                }
            ],
        },
        {
            "context": "what actually Appraisal is ?",
            "entities": [
                {
                    "entity_value": "Appraisal",
                    "entity_type": "Fin_Corp",
                    "start_index": 14,
                    "end_index": 23,
                }
            ],
        },
        {
            "context": "what do Prepaid Items mean, explain the details",
            "entities": [
                {
                    "entity_value": "Prepaid Items",
                    "entity_type": "Fin_Corp",
                    "start_index": 8,
                    "end_index": 21,
                }
            ],
        },
        {
            "context": "what do Principal mean, explain the details",
            "entities": [
                {
                    "entity_value": "Principal",
                    "entity_type": "Fin_Corp",
                    "start_index": 8,
                    "end_index": 17,
                }
            ],
        },
        {
            "context": "I'm sorry, I'm not familiar with the meaning of Buyers Agent . What does that mean?",
            "entities": [
                {
                    "entity_value": "Buyers Agent",
                    "entity_type": "Fin_Corp",
                    "start_index": 48,
                    "end_index": 60,
                }
            ],
        },
        {
            "context": "I'm sorry, I'm not familiar with the meaning of Payment Cap . What does that mean?",
            "entities": [
                {
                    "entity_value": "Payment Cap",
                    "entity_type": "Fin_Corp",
                    "start_index": 48,
                    "end_index": 59,
                }
            ],
        },
        {
            "context": "Hello, Can you expand Sellers Agent ?",
            "entities": [
                {
                    "entity_value": "Sellers Agent",
                    "entity_type": "Fin_Corp",
                    "start_index": 22,
                    "end_index": 35,
                }
            ],
        },
        {
            "context": "Hello, Can you expand Floor ?",
            "entities": [
                {
                    "entity_value": "Floor",
                    "entity_type": "Fin_Corp",
                    "start_index": 22,
                    "end_index": 27,
                }
            ],
        },
        {
            "context": "What is Default ?",
            "entities": [
                {
                    "entity_value": "Default",
                    "entity_type": "Fin_Corp",
                    "start_index": 8,
                    "end_index": 15,
                }
            ],
        },
        {
            "context": "What is Amortization ?",
            "entities": [
                {
                    "entity_value": "Amortization",
                    "entity_type": "Fin_Corp",
                    "start_index": 8,
                    "end_index": 20,
                }
            ],
        },
        {
            "context": "What does Annual Percentage Rate mean?",
            "entities": [
                {
                    "entity_value": "Annual Percentage Rate",
                    "entity_type": "Fin_Corp",
                    "start_index": 10,
                    "end_index": 32,
                }
            ],
        },
        {
            "context": "What does Site-Built Housing mean?",
            "entities": [
                {
                    "entity_value": "Site-Built Housing",
                    "entity_type": "Fin_Corp",
                    "start_index": 10,
                    "end_index": 28,
                }
            ],
        },
        {
            "context": "Can you define what Amortization stands for and what it means?",
            "entities": [
                {
                    "entity_value": "Amortization",
                    "entity_type": "Fin_Corp",
                    "start_index": 20,
                    "end_index": 32,
                }
            ],
        },
        {
            "context": "Can you define what Fixed Interest Rate stands for and what it means?",
            "entities": [
                {
                    "entity_value": "Fixed Interest Rate",
                    "entity_type": "Fin_Corp",
                    "start_index": 20,
                    "end_index": 39,
                }
            ],
        },
        {
            "context": "I was looking over loan application could you explain what is meant by Point ?",
            "entities": [
                {
                    "entity_value": "Point",
                    "entity_type": "Fin_Corp",
                    "start_index": 71,
                    "end_index": 76,
                }
            ],
        },
        {
            "context": "I was looking over loan application could you explain what is meant by Net Income ?",
            "entities": [
                {
                    "entity_value": "Net Income",
                    "entity_type": "Fin_Corp",
                    "start_index": 71,
                    "end_index": 81,
                }
            ],
        },
        {
            "context": "I dont know what Interest stands for could you explain it clearly to me please?",
            "entities": [
                {
                    "entity_value": "Interest",
                    "entity_type": "Fin_Corp",
                    "start_index": 17,
                    "end_index": 25,
                }
            ],
        },
        {
            "context": "I dont know what Multiple Listing Service stands for could you explain it clearly to me please?",
            "entities": [
                {
                    "entity_value": "Multiple Listing Service",
                    "entity_type": "Fin_Corp",
                    "start_index": 17,
                    "end_index": 41,
                }
            ],
        },
        {
            "context": "what Homeowners Warranty Program means",
            "entities": [
                {
                    "entity_value": "Homeowners Warranty Program",
                    "entity_type": "Fin_Corp",
                    "start_index": 5,
                    "end_index": 32,
                }
            ],
        },
        {
            "context": "what Condominium means",
            "entities": [
                {
                    "entity_value": "Condominium",
                    "entity_type": "Fin_Corp",
                    "start_index": 5,
                    "end_index": 16,
                }
            ],
        },
        {
            "context": "Why is knowing your Interest Cap important?",
            "entities": [
                {
                    "entity_value": "Interest Cap",
                    "entity_type": "Fin_Corp",
                    "start_index": 20,
                    "end_index": 32,
                }
            ],
        },
        {
            "context": "Why is knowing your Credit Bureau important?",
            "entities": [
                {
                    "entity_value": "Credit Bureau",
                    "entity_type": "Fin_Corp",
                    "start_index": 20,
                    "end_index": 33,
                }
            ],
        },
        {
            "context": "Please explain what you mean by Qualifying Ratios .",
            "entities": [
                {
                    "entity_value": "Qualifying Ratios",
                    "entity_type": "Fin_Corp",
                    "start_index": 32,
                    "end_index": 49,
                }
            ],
        },
        {
            "context": "Please explain what you mean by Closed-Ended Credit .",
            "entities": [
                {
                    "entity_value": "Closed-Ended Credit",
                    "entity_type": "Fin_Corp",
                    "start_index": 32,
                    "end_index": 51,
                }
            ],
        },
        {
            "context": "please explain what is VA Loan in detail.",
            "entities": [
                {
                    "entity_value": "VA Loan",
                    "entity_type": "Fin_Corp",
                    "start_index": 23,
                    "end_index": 30,
                }
            ],
        },
        {
            "context": "please explain what is Agent in detail.",
            "entities": [
                {
                    "entity_value": "Agent",
                    "entity_type": "Fin_Corp",
                    "start_index": 23,
                    "end_index": 28,
                }
            ],
        },
        {
            "context": "Could you please elaborate Lease-Purchase ?",
            "entities": [
                {
                    "entity_value": "Lease-Purchase",
                    "entity_type": "Fin_Corp",
                    "start_index": 27,
                    "end_index": 41,
                }
            ],
        },
        {
            "context": "Could you please elaborate Interest Rate ?",
            "entities": [
                {
                    "entity_value": "Interest Rate",
                    "entity_type": "Fin_Corp",
                    "start_index": 27,
                    "end_index": 40,
                }
            ],
        },
        {
            "context": "Can you explain Delinquency to me?",
            "entities": [
                {
                    "entity_value": "Delinquency",
                    "entity_type": "Fin_Corp",
                    "start_index": 16,
                    "end_index": 27,
                }
            ],
        },
        {
            "context": "Can you explain Balloon Mortgage to me?",
            "entities": [
                {
                    "entity_value": "Balloon Mortgage",
                    "entity_type": "Fin_Corp",
                    "start_index": 16,
                    "end_index": 32,
                }
            ],
        },
        {
            "context": "what does Prepaid Items really mean",
            "entities": [
                {
                    "entity_value": "Prepaid Items",
                    "entity_type": "Fin_Corp",
                    "start_index": 10,
                    "end_index": 23,
                }
            ],
        },
        {
            "context": "what does Loan-to-Value Ratio really mean",
            "entities": [
                {
                    "entity_value": "Loan-to-Value Ratio",
                    "entity_type": "Fin_Corp",
                    "start_index": 10,
                    "end_index": 29,
                }
            ],
        },
        {
            "context": "Can you explain to me,please,what Homeowners Warranty Program means,what it applies to,what is its purpose? Thank you",
            "entities": [
                {
                    "entity_value": "Homeowners Warranty Program",
                    "entity_type": "Fin_Corp",
                    "start_index": 34,
                    "end_index": 61,
                }
            ],
        },
        {
            "context": "Can you explain to me,please,what Balloon Mortgage means,what it applies to,what is its purpose? Thank you",
            "entities": [
                {
                    "entity_value": "Balloon Mortgage",
                    "entity_type": "Fin_Corp",
                    "start_index": 34,
                    "end_index": 50,
                }
            ],
        },
        {
            "context": "what's the meaning of Mortgagee and how can i use it?",
            "entities": [
                {
                    "entity_value": "Mortgagee",
                    "entity_type": "Fin_Corp",
                    "start_index": 22,
                    "end_index": 31,
                }
            ],
        },
        {
            "context": "what's the meaning of Prepayment Penalty and how can i use it?",
            "entities": [
                {
                    "entity_value": "Prepayment Penalty",
                    "entity_type": "Fin_Corp",
                    "start_index": 22,
                    "end_index": 40,
                }
            ],
        },
        {
            "context": "Ive not heard that before. What does Interest Cap mean?",
            "entities": [
                {
                    "entity_value": "Interest Cap",
                    "entity_type": "Fin_Corp",
                    "start_index": 37,
                    "end_index": 49,
                }
            ],
        },
        {
            "context": "Ive not heard that before. What does Lender mean?",
            "entities": [
                {
                    "entity_value": "Lender",
                    "entity_type": "Fin_Corp",
                    "start_index": 37,
                    "end_index": 43,
                }
            ],
        },
        {
            "context": "Can you elaborate on what Mortgage Banker is about?",
            "entities": [
                {
                    "entity_value": "Mortgage Banker",
                    "entity_type": "Fin_Corp",
                    "start_index": 26,
                    "end_index": 41,
                }
            ],
        },
        {
            "context": "Can you elaborate on what Assessment is about?",
            "entities": [
                {
                    "entity_value": "Assessment",
                    "entity_type": "Fin_Corp",
                    "start_index": 26,
                    "end_index": 36,
                }
            ],
        },
        {
            "context": "I've never heard of Due-on-Sale , can you explain it to me in an easy way for me to understand?",
            "entities": [
                {
                    "entity_value": "Due-on-Sale",
                    "entity_type": "Fin_Corp",
                    "start_index": 20,
                    "end_index": 31,
                }
            ],
        },
        {
            "context": "I've never heard of Trust , can you explain it to me in an easy way for me to understand?",
            "entities": [
                {
                    "entity_value": "Trust",
                    "entity_type": "Fin_Corp",
                    "start_index": 20,
                    "end_index": 25,
                }
            ],
        },
        {
            "context": "How does my Market Value effect me?",
            "entities": [
                {
                    "entity_value": "Market Value",
                    "entity_type": "Fin_Corp",
                    "start_index": 12,
                    "end_index": 24,
                }
            ],
        },
        {
            "context": "How does my Balloon Mortgage effect me?",
            "entities": [
                {
                    "entity_value": "Balloon Mortgage",
                    "entity_type": "Fin_Corp",
                    "start_index": 12,
                    "end_index": 28,
                }
            ],
        },
    ],
    "train_params": {"num_epoch": 10, "batch_size": 8, "LR": 0.02},
}

test_entity_training_fail = {
    "train_data": [],
    "train_params": {"num_epoch": 10, "batch_size": 8, "LR": 0.02},
}

test_entity_config_setup_ner = {"ner_model": "ner", "model_type": "LSTM"}

test_entity_config_setup_trf = {
    "ner_model": "prajjwal1/bert-tiny",
    "model_type": "TRFMODEL",
}

test_entity_config_setup_blank = {"ner_model": "None", "model_type": "LSTM"}
