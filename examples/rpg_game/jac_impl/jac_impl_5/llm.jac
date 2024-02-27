import:py from hugchat.login, Login;
import:py from hugchat, hugchat;

include:jac _secrets; # Email and password are included in a secrets.jac file

with entry {

    sign = Login(email, passwd);
    cookies = sign.login();

    cookie_path_dir = "./cookies_snapshot";
    sign.saveCookiesToDir(cookie_path_dir);

    # start a new huggingchat connection
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict());

    # start a new conversation
    chatbot.delete_all_conversations();
    id = chatbot.new_conversation();
    chatbot.change_conversation(id);
    chatbot.switch_llm(2);

    # enter your message here
    msg = 'Give me a random integer between 10 and 10000, Just the integer is sufficient no need prefixes or suffixes';

    # print the response
    print(chatbot.chat(msg));
}