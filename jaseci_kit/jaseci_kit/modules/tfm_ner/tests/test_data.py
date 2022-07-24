# flake8: noqa
test_train_config = {"training_parameters": {"EPOCHS": 50}}

test_model_config = {"model_parameters": {"model_save_path": "modeloutput1"}}


test_test_data = {"text": "Britain backed Fischler's proposal ."}

test_entities = [
    {
        "text": "britain",
        "entity": "LOC",
        "score": 0.5076541304588318,
        "start": 0,
        "end": 7,
    },
    {
        "text": "fischler",
        "entity": "ORG",
        "score": 0.36676135659217837,
        "start": 15,
        "end": 23,
    },
]
test_training_data = [
    {
        "context": "Australian coach Geoff Marsh said he was impressed with the competitiveness of the opposition .",
        "entities": [
            {
                "entity_value": "Australian",
                "entity_type": "MISC",
                "start_index": 0,
                "end_index": 10,
            },
            {
                "entity_value": "Geoff Marsh",
                "entity_type": "PER",
                "start_index": 17,
                "end_index": 28,
            },
        ],
    },
    {"context": '" We were made to sweat to win , " he said .', "entities": []},
    {
        "context": "ONE ROMANIAN DIES IN BUS CRASH IN BULGARIA .",
        "entities": [
            {
                "entity_value": "ROMANIAN",
                "entity_type": "MISC",
                "start_index": 4,
                "end_index": 12,
            },
            {
                "entity_value": "BULGARIA",
                "entity_type": "LOC",
                "start_index": 34,
                "end_index": 42,
            },
        ],
    },
    {
        "context": "SOFIA 1996-08-22",
        "entities": [
            {
                "entity_value": "SOFIA",
                "entity_type": "LOC",
                "start_index": 0,
                "end_index": 5,
            }
        ],
    },
    {
        "context": "One Romanian passenger was killed , and 14 others were injured on Thursday when a Romanian-registered bus collided with a Bulgarian one in northern Bulgaria , police said .",
        "entities": [
            {
                "entity_value": "Romanian",
                "entity_type": "MISC",
                "start_index": 4,
                "end_index": 12,
            },
            {
                "entity_value": "Romanian-registered",
                "entity_type": "MISC",
                "start_index": 82,
                "end_index": 101,
            },
            {
                "entity_value": "Bulgarian",
                "entity_type": "MISC",
                "start_index": 122,
                "end_index": 131,
            },
            {
                "entity_value": "Bulgaria",
                "entity_type": "LOC",
                "start_index": 122,
                "end_index": 130,
            },
        ],
    },
    {
        "context": "The two buses collided head on at 5 o'clock this morning on the road between the towns of Rousse and Veliko Tarnovo , police said .",
        "entities": [
            {
                "entity_value": "Rousse",
                "entity_type": "LOC",
                "start_index": 90,
                "end_index": 96,
            },
            {
                "entity_value": "Veliko Tarnovo",
                "entity_type": "LOC",
                "start_index": 101,
                "end_index": 115,
            },
        ],
    },
    {
        "context": "A Romanian woman Maria Marco , 35 , was killed .",
        "entities": [
            {
                "entity_value": "Romanian",
                "entity_type": "MISC",
                "start_index": 2,
                "end_index": 10,
            },
            {
                "entity_value": "Maria Marco",
                "entity_type": "PER",
                "start_index": 17,
                "end_index": 28,
            },
        ],
    },
    {"context": "The accident was being investigated , police added .", "entities": []},
    {
        "context": "-- Sofia Newsroom , 359-2-84561",
        "entities": [
            {
                "entity_value": "Sofia Newsroom",
                "entity_type": "ORG",
                "start_index": 3,
                "end_index": 17,
            }
        ],
    },
    {
        "context": "OFFICIAL JOURNAL CONTENTS - OJ L 211 OF AUGUST 21 , 1996 .",
        "entities": [
            {
                "entity_value": "OFFICIAL JOURNAL",
                "entity_type": "ORG",
                "start_index": 0,
                "end_index": 16,
            },
            {
                "entity_value": "OJ",
                "entity_type": "ORG",
                "start_index": 28,
                "end_index": 30,
            },
        ],
    },
    {"context": "*", "entities": []},
    {
        "context": "( Note - contents are displayed in reverse order to that in the printed Journal )",
        "entities": [
            {
                "entity_value": "Journal",
                "entity_type": "ORG",
                "start_index": 72,
                "end_index": 79,
            }
        ],
    },
    {"context": "*", "entities": []},
    {
        "context": "Corrigendum to Commission Regulation ( EC ) No 1464/96 of 25 July 1996 relating to a standing invitation to tender to determine levies and / or refunds on exports of white sugar ( OJ No L 187 of 26.7.1996 )",
        "entities": [
            {
                "entity_value": "Commission Regulation",
                "entity_type": "MISC",
                "start_index": 15,
                "end_index": 36,
            },
            {
                "entity_value": "EC",
                "entity_type": "ORG",
                "start_index": 39,
                "end_index": 41,
            },
        ],
    },
    {
        "context": "Corrigendum to Commission Regulation ( EC ) No 658/96 of 9 April 1996 on certain conditions for granting compensatory payments under the support system for producers of certain arable crops ( OJ No L 91 of 12.4.1996 )",
        "entities": [
            {
                "entity_value": "Commission Regulation",
                "entity_type": "MISC",
                "start_index": 15,
                "end_index": 36,
            },
            {
                "entity_value": "EC",
                "entity_type": "ORG",
                "start_index": 39,
                "end_index": 41,
            },
            {
                "entity_value": "OJ",
                "entity_type": "ORG",
                "start_index": 192,
                "end_index": 194,
            },
        ],
    },
    {
        "context": "Commission Regulation ( EC ) No 1663/96 of 20 August 1996 establishing the standard import values for determining the entry price of certain fruit and vegetables END OF DOCUMENT .",
        "entities": [
            {
                "entity_value": "Commission Regulation",
                "entity_type": "MISC",
                "start_index": 0,
                "end_index": 21,
            },
            {
                "entity_value": "EC",
                "entity_type": "ORG",
                "start_index": 24,
                "end_index": 26,
            },
        ],
    },
    {
        "context": "In Home Health to appeal payment denial .",
        "entities": [
            {
                "entity_value": "In Home Health",
                "entity_type": "ORG",
                "start_index": 0,
                "end_index": 14,
            }
        ],
    },
    {
        "context": "MINNETONKA , Minn .",
        "entities": [
            {
                "entity_value": "MINNETONKA",
                "entity_type": "LOC",
                "start_index": 0,
                "end_index": 10,
            },
            {
                "entity_value": "Minn",
                "entity_type": "LOC",
                "start_index": 13,
                "end_index": 17,
            },
        ],
    },
    {"context": "1996-08-22", "entities": []},
    {
        "context": "In Home Health Inc said on Thursday it will appeal to the U.S. Federal District Court in Minneapolis a decision by the Health Care Financing Administration ( HCFA ) that denied reimbursement of certain costs under Medicaid .",
        "entities": [
            {
                "entity_value": "In Home Health Inc",
                "entity_type": "ORG",
                "start_index": 0,
                "end_index": 18,
            },
            {
                "entity_value": "U.S. Federal District Court",
                "entity_type": "ORG",
                "start_index": 58,
                "end_index": 85,
            },
            {
                "entity_value": "Minneapolis",
                "entity_type": "LOC",
                "start_index": 89,
                "end_index": 100,
            },
            {
                "entity_value": "Health Care Financing Administration",
                "entity_type": "ORG",
                "start_index": 119,
                "end_index": 155,
            },
            {
                "entity_value": "HCFA",
                "entity_type": "ORG",
                "start_index": 158,
                "end_index": 162,
            },
            {
                "entity_value": "Medicaid",
                "entity_type": "MISC",
                "start_index": 214,
                "end_index": 222,
            },
        ],
    },
    {
        "context": "The HCFA Administrator reversed a previously favorable decision regarding the reimbursement of costs related to the company 's community liaison personnel , it added .",
        "entities": [
            {
                "entity_value": "HCFA",
                "entity_type": "ORG",
                "start_index": 4,
                "end_index": 8,
            }
        ],
    },
    {
        "context": "The company said it continues to believe the majority of the community liaison costs are coverable under the terms of the Medicare program .",
        "entities": [
            {
                "entity_value": "Medicare",
                "entity_type": "MISC",
                "start_index": 122,
                "end_index": 130,
            }
        ],
    },
    {
        "context": '" We are disappointed with the administrator \'s decision but we continue to be optimistic regarding an ultimate favorable resolution , " Mark Gildea , chief executive officer , said in a statement .',
        "entities": [
            {
                "entity_value": "Mark Gildea",
                "entity_type": "PER",
                "start_index": 137,
                "end_index": 148,
            }
        ],
    },
    {
        "context": "In Home Health said it previously recorded a reserve equal to 16 percent of all revenue related to the community liaison costs .",
        "entities": [
            {
                "entity_value": "In Home Health",
                "entity_type": "ORG",
                "start_index": 0,
                "end_index": 14,
            }
        ],
    },
    {
        "context": "Separately , In Home Health said the U.S. District Court in Minneapolis ruled in its favor regarding the reimbursement of certain interest expenses .",
        "entities": [
            {
                "entity_value": "In Home Health",
                "entity_type": "ORG",
                "start_index": 13,
                "end_index": 27,
            },
            {
                "entity_value": "U.S. District Court",
                "entity_type": "ORG",
                "start_index": 37,
                "end_index": 56,
            },
            {
                "entity_value": "Minneapolis",
                "entity_type": "LOC",
                "start_index": 60,
                "end_index": 71,
            },
        ],
    },
    {
        "context": "This decision will result in the reimbursement by Medicare of $ 81,000 in disputed costs .",
        "entities": [
            {
                "entity_value": "Medicare",
                "entity_type": "MISC",
                "start_index": 50,
                "end_index": 58,
            }
        ],
    },
    {
        "context": '" This is our first decision in federal distrct court regarding a dispute with Medicare , " Gildea said . "',
        "entities": [
            {
                "entity_value": "Medicare",
                "entity_type": "MISC",
                "start_index": 79,
                "end_index": 87,
            },
            {
                "entity_value": "Gildea",
                "entity_type": "PER",
                "start_index": 92,
                "end_index": 98,
            },
        ],
    },
    {
        "context": 'We are extremely pleased with this decision and we recognize it as a significant step toward resolution of our outstanding Medicare disputes . "',
        "entities": [
            {
                "entity_value": "Medicare",
                "entity_type": "MISC",
                "start_index": 123,
                "end_index": 131,
            }
        ],
    },
    {
        "context": "-- Chicago Newsdesk 312-408-8787",
        "entities": [
            {
                "entity_value": "Chicago Newsdesk",
                "entity_type": "ORG",
                "start_index": 3,
                "end_index": 19,
            }
        ],
    },
    {
        "context": "Oppenheimer Capital to review Oct. div .",
        "entities": [
            {
                "entity_value": "Oppenheimer Capital",
                "entity_type": "ORG",
                "start_index": 0,
                "end_index": 19,
            }
        ],
    },
    {
        "context": "NEW YORK 1996-08-22",
        "entities": [
            {
                "entity_value": "NEW YORK",
                "entity_type": "LOC",
                "start_index": 0,
                "end_index": 8,
            }
        ],
    },
    {
        "context": "Oppenheimer Capital LP said on Thursday it will review its cash distribution rate for the October quarterly distribution , assuming continued favorable results .",
        "entities": [
            {
                "entity_value": "Oppenheimer Capital LP",
                "entity_type": "ORG",
                "start_index": 0,
                "end_index": 22,
            }
        ],
    },
    {
        "context": "Best sees Q2 loss similar to Q1 loss .",
        "entities": [
            {
                "entity_value": "Best",
                "entity_type": "ORG",
                "start_index": 0,
                "end_index": 4,
            }
        ],
    },
    {
        "context": "RICHMOND , Va .",
        "entities": [
            {
                "entity_value": "RICHMOND",
                "entity_type": "LOC",
                "start_index": 0,
                "end_index": 8,
            },
            {
                "entity_value": "Va",
                "entity_type": "LOC",
                "start_index": 11,
                "end_index": 13,
            },
        ],
    },
    {"context": "1996-08-22", "entities": []},
    {
        "context": "Best Products Co Chairman and Chief Executive Daniel Levy said Thursday he expected the company 's second-quarter results to be similar to the $ 34.6 million loss posted in the first quarter .",
        "entities": [
            {
                "entity_value": "Best Products Co",
                "entity_type": "ORG",
                "start_index": 0,
                "end_index": 16,
            },
            {
                "entity_value": "Daniel Levy",
                "entity_type": "PER",
                "start_index": 46,
                "end_index": 57,
            },
        ],
    },
    {
        "context": "He also told Reuters before the retailer 's annual meeting that the second quarter could be better than the first quarter ended May 4 . \"",
        "entities": [
            {
                "entity_value": "Reuters",
                "entity_type": "ORG",
                "start_index": 13,
                "end_index": 20,
            }
        ],
    },
    {
        "context": "Levy said seeking bankruptcy protection was not under consideration .",
        "entities": [
            {
                "entity_value": "Levy",
                "entity_type": "PER",
                "start_index": 0,
                "end_index": 4,
            }
        ],
    },
    {
        "context": "Best emerged from Chapter 11 bankruptcy protection in June 1994 after 3-1/2 years .",
        "entities": [
            {
                "entity_value": "Best",
                "entity_type": "ORG",
                "start_index": 0,
                "end_index": 4,
            },
            {
                "entity_value": "Chapter 11",
                "entity_type": "MISC",
                "start_index": 18,
                "end_index": 28,
            },
        ],
    },
    {
        "context": '" Bankruptcy is always possible , particularly when you lose what we are going to lose in the first half of this year , " Levy said . "',
        "entities": [
            {
                "entity_value": "Levy",
                "entity_type": "PER",
                "start_index": 122,
                "end_index": 126,
            }
        ],
    },
    {
        "context": "The Richmond-based retailer lost $ 95.7 million in the fiscal year ended February 3 .",
        "entities": [
            {
                "entity_value": "Richmond-based",
                "entity_type": "MISC",
                "start_index": 4,
                "end_index": 18,
            }
        ],
    },
    {
        "context": "Levy said that Best planned to open two new stores this fall .",
        "entities": [
            {
                "entity_value": "Levy",
                "entity_type": "PER",
                "start_index": 0,
                "end_index": 4,
            },
            {
                "entity_value": "Best",
                "entity_type": "ORG",
                "start_index": 15,
                "end_index": 19,
            },
        ],
    },
    {
        "context": "At the time , Best said it did not plan to open any new stores this fall .",
        "entities": [
            {
                "entity_value": "Best",
                "entity_type": "ORG",
                "start_index": 14,
                "end_index": 18,
            }
        ],
    },
    {"context": "It currently operates 169 stores in 23 states .", "entities": []},
    {
        "context": "For last year 's second quarter , which ended July 29 , 1995 , Best posted a loss of $ 7.1 million , or $ 0.23 per share , on sales of $ 311.9 million .",
        "entities": [
            {
                "entity_value": "Best",
                "entity_type": "ORG",
                "start_index": 63,
                "end_index": 67,
            }
        ],
    },
    {"context": "Measles exposure can lead to bowel disease - study .", "entities": []},
    {
        "context": "LONDON 1996-08-23",
        "entities": [
            {
                "entity_value": "LONDON",
                "entity_type": "LOC",
                "start_index": 0,
                "end_index": 6,
            }
        ],
    },
    {
        "context": "Women who get measles while pregnant may have babies at higher risk of Crohn 's disease , a debilitating bowel disorder , researchers said on Friday .",
        "entities": [
            {
                "entity_value": "Crohn",
                "entity_type": "PER",
                "start_index": 71,
                "end_index": 76,
            }
        ],
    },
    {
        "context": "Three out of four Swedish babies born to mothers who caught measles developed serious cases of Crohn 's disease , the researchers said .",
        "entities": [
            {
                "entity_value": "Swedish",
                "entity_type": "MISC",
                "start_index": 18,
                "end_index": 25,
            },
            {
                "entity_value": "Crohn",
                "entity_type": "PER",
                "start_index": 95,
                "end_index": 100,
            },
        ],
    },
    {
        "context": "Dr Andrew Wakefield of the Royal Free Hospital School of Medicine and colleagues screened 25,000 babies delivered at University Hospital , Uppsala , between 1940 and 1949 .",
        "entities": [
            {
                "entity_value": "Andrew Wakefield",
                "entity_type": "PER",
                "start_index": 3,
                "end_index": 19,
            },
            {
                "entity_value": "Royal Free Hospital School of Medicine",
                "entity_type": "LOC",
                "start_index": 27,
                "end_index": 65,
            },
            {
                "entity_value": "University Hospital",
                "entity_type": "LOC",
                "start_index": 117,
                "end_index": 136,
            },
            {
                "entity_value": "Uppsala",
                "entity_type": "LOC",
                "start_index": 139,
                "end_index": 146,
            },
        ],
    },
    {
        "context": "\" Three of the four children had Crohn 's disease , \" Wakefield 's group wrote in the Lancet medical journal .",
        "entities": [
            {
                "entity_value": "Crohn",
                "entity_type": "PER",
                "start_index": 33,
                "end_index": 38,
            },
            {
                "entity_value": "Wakefield",
                "entity_type": "PER",
                "start_index": 54,
                "end_index": 63,
            },
            {
                "entity_value": "Lancet",
                "entity_type": "ORG",
                "start_index": 86,
                "end_index": 92,
            },
        ],
    },
    {
        "context": "Crohn 's is an inflammation of the bowel that can sometimes require surgery .",
        "entities": [
            {
                "entity_value": "Crohn",
                "entity_type": "PER",
                "start_index": 0,
                "end_index": 5,
            }
        ],
    },
    {"context": "Exposure to viruses can often cause birth defects .", "entities": []},
    {
        "context": "Most notably , women who get rubella ( German measles ) have a high risk of a stillborn baby .",
        "entities": [
            {
                "entity_value": "German",
                "entity_type": "MISC",
                "start_index": 39,
                "end_index": 45,
            }
        ],
    },
    {
        "context": "All the key numbers - CBI August industrial trends .",
        "entities": [
            {
                "entity_value": "CBI",
                "entity_type": "ORG",
                "start_index": 22,
                "end_index": 25,
            }
        ],
    },
    {
        "context": "LONDON 1996-08-23",
        "entities": [
            {
                "entity_value": "LONDON",
                "entity_type": "LOC",
                "start_index": 0,
                "end_index": 6,
            }
        ],
    },
    {
        "context": "Following are key data from the August monthly survey of trends in UK manufacturing by the Confederation of British Industry ( CBI ) .",
        "entities": [
            {
                "entity_value": "UK",
                "entity_type": "LOC",
                "start_index": 67,
                "end_index": 69,
            },
            {
                "entity_value": "Confederation of British Industry",
                "entity_type": "ORG",
                "start_index": 91,
                "end_index": 124,
            },
            {
                "entity_value": "CBI",
                "entity_type": "ORG",
                "start_index": 127,
                "end_index": 130,
            },
        ],
    },
    {
        "context": "CBI MONTHLY TRENDS ENQUIRY ( a ) AUG JULY JUNE MAY",
        "entities": [
            {
                "entity_value": "CBI",
                "entity_type": "ORG",
                "start_index": 0,
                "end_index": 3,
            }
        ],
    },
    {
        "context": "The survey was conducted between July 23 and August 14 and involved 1,305 companies , representing 50 industries , accounting for around half of the UK 's manufactured exports and some two million employees .",
        "entities": [
            {
                "entity_value": "UK",
                "entity_type": "LOC",
                "start_index": 149,
                "end_index": 151,
            }
        ],
    },
    {
        "context": "-- Rosemary Bennett , London Newsroom +44 171 542 7715",
        "entities": [
            {
                "entity_value": "Rosemary Bennett",
                "entity_type": "PER",
                "start_index": 3,
                "end_index": 19,
            },
            {
                "entity_value": "London Newsroom",
                "entity_type": "ORG",
                "start_index": 22,
                "end_index": 37,
            },
        ],
    },
    {
        "context": "London shipsales .",
        "entities": [
            {
                "entity_value": "London",
                "entity_type": "LOC",
                "start_index": 0,
                "end_index": 6,
            }
        ],
    },
    {
        "context": "LONDON 1996-08-22",
        "entities": [
            {
                "entity_value": "LONDON",
                "entity_type": "LOC",
                "start_index": 0,
                "end_index": 6,
            }
        ],
    },
    {
        "context": "Iron Gippsland - ( built 1989 ) 87,241 dwt sold to Greek buyers for $ 30 million .",
        "entities": [
            {
                "entity_value": "Iron Gippsland",
                "entity_type": "MISC",
                "start_index": 0,
                "end_index": 14,
            },
            {
                "entity_value": "Greek",
                "entity_type": "MISC",
                "start_index": 51,
                "end_index": 56,
            },
        ],
    },
    {
        "context": "Sairyu Maru No : 2 - ( built 1982 ) 60,960 dwt sold to Greek buyers for $ 15.5 million .",
        "entities": [
            {
                "entity_value": "Sairyu Maru No : 2",
                "entity_type": "MISC",
                "start_index": 0,
                "end_index": 18,
            },
            {
                "entity_value": "Greek",
                "entity_type": "MISC",
                "start_index": 55,
                "end_index": 60,
            },
        ],
    },
    {
        "context": "Stainless Fighter - ( built 1970 ) 21,718 dwt sold at auction for $ 6 million .",
        "entities": [
            {
                "entity_value": "Stainless Fighter",
                "entity_type": "MISC",
                "start_index": 0,
                "end_index": 17,
            }
        ],
    },
    {
        "context": "LONDON 1996-08-22",
        "entities": [
            {
                "entity_value": "LONDON",
                "entity_type": "LOC",
                "start_index": 0,
                "end_index": 6,
            }
        ],
    },
    {
        "context": "Garlic pills may not lower blood cholesterol and studies that show they do may be flawed , British researchers have reported .",
        "entities": [
            {
                "entity_value": "British",
                "entity_type": "MISC",
                "start_index": 91,
                "end_index": 98,
            }
        ],
    },
    {
        "context": "A study by a team of doctors at Oxford University has found people with high blood cholesterol do not benefit significantly from taking garlic tablets .",
        "entities": [
            {
                "entity_value": "Oxford University",
                "entity_type": "ORG",
                "start_index": 32,
                "end_index": 49,
            }
        ],
    },
    {
        "context": 'There were no significant differences between the groups receiving garlic and placebo , " they wrote in the Journal of the Royal College of Physicians .',
        "entities": [
            {
                "entity_value": "Journal of the Royal College of Physicians",
                "entity_type": "ORG",
                "start_index": 108,
                "end_index": 150,
            }
        ],
    },
    {
        "context": "But the Oxford team disputed these findings and said either previous trials may have been interpreted incorrectly , those taking part were not given special diets beforehand or the duration of the studies may have been too short .",
        "entities": [
            {
                "entity_value": "Oxford",
                "entity_type": "LOC",
                "start_index": 8,
                "end_index": 14,
            }
        ],
    },
    {
        "context": "The six-month trial was funded by the British Heart Foundation and Lichtwer Pharma GmbH , which makes Kwai brand garlic tablets .",
        "entities": [
            {
                "entity_value": "British Heart Foundation",
                "entity_type": "ORG",
                "start_index": 38,
                "end_index": 62,
            },
            {
                "entity_value": "Lichtwer Pharma GmbH",
                "entity_type": "ORG",
                "start_index": 67,
                "end_index": 87,
            },
            {
                "entity_value": "Kwai",
                "entity_type": "MISC",
                "start_index": 102,
                "end_index": 106,
            },
        ],
    },
    {
        "context": "-- London Newsroom +44 171 542 7950",
        "entities": [
            {
                "entity_value": "London Newsroom",
                "entity_type": "ORG",
                "start_index": 3,
                "end_index": 18,
            }
        ],
    },
    {
        "context": "Britain gives aid to volcano-hit Caribbean island .",
        "entities": [
            {
                "entity_value": "Britain",
                "entity_type": "LOC",
                "start_index": 0,
                "end_index": 7,
            },
            {
                "entity_value": "Caribbean",
                "entity_type": "LOC",
                "start_index": 33,
                "end_index": 42,
            },
        ],
    },
    {
        "context": "LONDON 1996-08-22",
        "entities": [
            {
                "entity_value": "LONDON",
                "entity_type": "LOC",
                "start_index": 0,
                "end_index": 6,
            }
        ],
    },
]
