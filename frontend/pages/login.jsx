import { useState } from "react";
import Link from "next/link";
import Router from "next/router";
import Layout from "../components/Layout";
import { useAuth } from "../services/auth";

const loginApi = async (username, password) => {
  const resp = await fetch("/api/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  if (resp.status !== 200) {
    throw new Error(await resp.text());
  }
  Router.push("/me");
};

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const { loading, isAuthenticated, login } = useAuth();

  const handleSubmit = async (
    event
  ) => {
    event.preventDefault();
    
    setErrorMessage("");
    try {
      const resp = await login(username, password);
      if (resp.status === 401) {
        setErrorMessage("Invalid login credentials");
      }
    } catch (error) {
      console.error(error);
      // TODO: actually parse api 400 error messages
      setErrorMessage(error.message);
    }
  };

  if (!loading && isAuthenticated) Router.push("/");

  return (
    <Layout>
      <form className="w-full mx-auto flex flex-col max-w-sm pt-4" onSubmit={handleSubmit}>
        <div className="mb-16 flex flex-col">
            <h1 className="text-4xl text-center text-white font-extrabold">
              Foodbank login
            </h1>
        </div>
        <div className="mb-6 flex flex-col">
            <label
              className="block text-accents-7 font-bold mb-3 pr-4"
              htmlFor="email"
            >
              Email
            </label>
            <input
              type="text"
              className="bg-accents-1 appearance-none border-2 border-accents-1 rounded w-full py-2 px-4 text- leading-tight focus:outline-none focus:bg-accents-2 focus:border-accents-4"
              id="email"
              name="email"
              value={username}
              onChange={(e) =>
                setUsername(e.target.value)
              }
            />
        </div>
        <div className="mb-6 flex flex-col">
            <label
              className="block text-accents-7 font-bold mb-3 pr-4"
              htmlFor="password"
            >
              Password
            </label>
            <input
              type="password"
              className="bg-accents-1 appearance-none border-2 border-accents-1 rounded w-full py-2 px-4 text- leading-tight focus:outline-none focus:bg-accents-2 focus:border-accents-4"
              id="password"
              name="password"
              value={password}
              onChange={(e) =>
                setPassword(e.target.value)
              }
            />
        </div>
        <div className="flex justify-center mt-6">
            <button
              className="shadow bg-accents-0 hover:bg-accents-1 transition-colours duration-200 focus:shadow-outline focus:outline-none text-white font-bold py-2 px-4 rounded-lg"
              type="submit"
            >
              Login
            </button>
        </div>
        {errorMessage ? (
          <div className="flex justify-center">
            <div className="pt-8">
              <p className="text-center text-red-400">Error: {errorMessage}</p>
            </div>
          </div>
        ) : null}
        <div className="flex justify-center">
          <div className="pt-8">
            <p className="text-center text-accents-6">
              Is your foodbank still not registered?<br />
              <Link href="/signup">
                <a className="font-bold">Sign up</a>
              </Link>
              .
            </p>
          </div>
        </div>
      </form>
    </Layout>
  );
};

export default Login;
