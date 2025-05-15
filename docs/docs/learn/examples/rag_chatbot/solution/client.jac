import streamlit as st;
import requests;

def bootstrap_frontend (token: str) {
    st.write("Welcome to your Demo Agent!");

    # Initialize chat history
    if "messages" not in st.session_state {
        st.session_state.messages = [];
    }

    for message in st.session_state.messages {
        with st.chat_message(message["role"]) {
            st.markdown(message["content"]);
        }
    }

    if prompt := st.chat_input("What is up?") {
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt});

        # Display user message in chat message container
        with st.chat_message("user") {
            st.markdown(prompt);
        }

        # Display assistant response in chat message container
        with st.chat_message("assistant") {

            # Call walker API
            response = requests.post("http://localhost:8000/walker/interact", json={"message": prompt, "session_id": "123"},
                headers={"Authorization": f"Bearer {token}"}
            );

            if response.status_code == 200 {
                response = response.json();
                print(response);
                st.write(response["reports"][0]["response"]);

                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response["reports"][0]["response"]});
            }
        }
    }
}

with entry {

    INSTANCE_URL = "http://localhost:8000";
    TEST_USER_EMAIL = "test@mail.com";
    TEST_USER_PASSWORD = "password";

    response = requests.post(
        f"{INSTANCE_URL}/user/login",
        json={"email": TEST_USER_EMAIL, "password": TEST_USER_PASSWORD}
    );

    if response.status_code != 200 {
        # Try registering the user if login fails
        response = requests.post(
            f"{INSTANCE_URL}/user/register",
            json={
                "email": TEST_USER_EMAIL,
                "password": TEST_USER_PASSWORD
            }
        );
        assert response.status_code == 201;

        response = requests.post(
            f"{INSTANCE_URL}/user/login",
            json={"email": TEST_USER_EMAIL, "password": TEST_USER_PASSWORD}
        );
        assert response.status_code == 200;
    }

    token = response.json()["token"];

    print("Token:", token);

    bootstrap_frontend(token);
}