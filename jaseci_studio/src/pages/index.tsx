import Head from "next/head";
import { LoginForm } from "../components/LoginForm";
import useUserInfo from "../hooks/useUserInfo";

function IndexPage() {
  return (
    <div>
      <Head>
        <title>Login</title>
      </Head>
      <LoginForm></LoginForm>
    </div>
  );
}

export default IndexPage;
