# import:py from hugchat.login, Login;
# import:py from hugchat, hugchat;

# include:jac _secrets; # Email and password are included in a secrets.jac file

# with entry {

#     sign = Login(email, passwd);
#     cookies = sign.login();

#     cookie_path_dir = "./cookies_snapshot";
#     sign.saveCookiesToDir(cookie_path_dir);

#     # start a new huggingchat connection
#     chatbot = hugchat.ChatBot(cookies=cookies.get_dict());

#     # start a new conversation
#     chatbot.delete_all_conversations();
#     id = chatbot.new_conversation();
#     chatbot.change_conversation(id);
#     chatbot.switch_llm(2);

#     # enter your message here
#     msg = 'Give me a random integer between 10 and 10000, Just the integer is sufficient no need prefixes or suffixes';

#     # print the response
#     print(chatbot.chat(msg));
# }

import:py openai;
import:py from openai, ChatCompletion;
import:py re;
import:py os;

import:py from typing, List;
import:py from enum, Enum;

obj model {
    has openai_api_key:str = os.getenv('OPENAI_API_KEY');

    can infer(prompt:str) {
        return openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        ).choices[0].message.content;

    }
}

glob PersonalityType = Enum('PersonalityType', ['EXTROVERTED', 'INTROVERTED']);

obj Person{
    has name:str,
        journal:List[str] = [],
        bio:str = "";

    can PersonalityCheck -> PersonalityType {
        prompt = ""
        "[System Prompt]"
        "This is an operation you must perform and return the output values. Neither, the methodology, extra sentences nor the code are not needed."

        "[Information]"
        f"Name of the Person (Str) (name): {<self>.name}"
        f"Journal Entries (List[str]) (journal): {<self>.journal}"
        f"Bio (Str) (bio): {<self>.bio}"

        "[Inputs and Input Type Information]"
        "None"

        "[Output Type]"
        "PersonalityType"

        "[Output Type Explanations]"
        "Enum PersonalityType:  options - PersonalityType.EXTROVERTED, PersonalityType.INTROVERTED 'Describes the personality of a person'"

        "[Action]"
        "Select the most appropriate personality type based on the Journal Entries and Biography if given else use general knowledge."

        "Reason and return the output result(s) only, adhering to the provided Type in the following format"

        "[Reasoning] <Reason>"
        "[Output] <Result>";

        response = llm.infer(prompt);
        personality_str = re.search(r"\[Output\] (.+)", response).group(1);
        return <self>.convert_to_enum(personality_str.strip());
    }

    can DeathCheck{
        return NotImplemented;
    }

    # can get_info -> (PersonalityType, int) {
    #     prompt= """
    #     [System Prompt]
    #     This is an operation you must perform and return the output values. Neither, the methodology, extra sentences nor the code are not needed.

    #     [Information]
    #     Name of the Person (Str) (name): {self.name}
    #     Journal Entries (List[str]) (journal): {self.journal}
    #     Bio (Str) (bio): {self.bio}

    #     [Inputs and Input Type Information]
    #     None

    #     [Output Type]
    #     Tuple type variable: (PersonalityType, int)

    #     [Output Type Explanations]
    #     Enum PersonalityType:  options - PersonalityType.EXTROVERTED, PersonalityType.INTROVERTED 'Describes the personality of a person'
    #     int

    #     [Action]
    #     Select the most appropriate personality type based on the Journal Entries and Biography if given else use general knowledge. Also, check if the person is dead, and if so, provide the year of death

    #     Reason and return the output result(s) only, adhering to the provided Type in the following format

    #     [Reasoning] <Reason>
    #     [Output] <Result>
    #     """;
    #     response = llm.enfer(prompt);

    #     result_str = re.search(r"\[Output\] (.+)", response).group(1);
    #     personality_str, year_of_death = result_str.replace("(", "").replace(")", "").split(", ");
    #     return (<self>.convert_to_enum(personality_str.strip()) , int(year_of_death));
    # }

    can convert_to_enum(personality: str) {
        if personality == "PersonalityType.EXTROVERTED"{
            return PersonalityType.EXTROVERTED;
        }
        else{
            return PersonalityType.INTROVERTED;
        }
    }
}

with entry {
    llm = model();

    einstein = Person(name = "Einstein");
    chandra = Person(name = "Chandra", journal = ["Chandra likes to party", "He likes to travel"], bio = "Chandra is died in 2021");

    print(einstein.PersonalityCheck());
    print(chandra.PersonalityCheck());
    # print(chandra.get_info());
}