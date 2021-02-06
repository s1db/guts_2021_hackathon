import Layout from "../components/Layout";
import { useState } from "react";
import Link from "next/link";
import Router from "next/router";
import { useAuth } from "../services/auth";
import cn from "classnames";
import { getPostcodeInfo } from '../services/FoobanksApi.js'

const signUpApi = async (email, password) => {
  const resp = await fetch("/api/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (resp.status !== 200) {
    throw new Error(await resp.text());
  }
  Router.push("/me");
};

const Signup = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const { signUp } = useAuth();
  const [address1, setAddress1] = useState("")
  const [address2, setAddress2] = useState("")
  const [postcode, setPostcode] = useState("")
  const [phone, setPhone] = useState("")
  const [postcodeError, setPostcodeError] = useState(null)

  const handleSubmit = async (
    event
  ) => {
    event.preventDefault();
    setErrorMessage("");

    const postcodeResult = await handleSearchPostcode()
    console.log('PSč result: ', postcodeResult)
    if (!postcodeResult) {
      return
    }


    console.log(postcodeResult)
    const data = {
      email ,
      password ,
      charityname: name ,
      postcode: postcodeResult.postcode,
      latitude: postcodeResult.latutide,
      longitude: postcodeResult.longitude,
      address: address1,
      address2: address2,
      phone,
    }

    try {
      const resp = await signUp(data);
      if (resp.status === 401) {
        setErrorMessage("Invalid login credentials");
      }
    } catch (error) {
      console.error(error);
      // TODO: actually parse api 400 error messages
      setErrorMessage(error.message);
    }
  };


  const handleSearchPostcode = async () => {

    setPostcodeError(null);
    
    if (postcode.length < 3 || postcode.length > 9) {
      setPostcodeError("The postcode is invalid.")
      return
    }

    try {

      const result = await getPostcodeInfo(postcode)

      if (result.postcode) {

        return result
      } else {
        setPostcodeError("The postcode is invalid.")
        return false
      }

    } catch (e) {
      console.log('error: ', e)
      return false
      setPostcodeError("The postcode is invalid.")
    }
  }
  const handlePostcodeChange = (target) => {
    setPostcodeError(null);
    setPostcode(target)
  }

  // if (!loading && isAuthenticated) Router.push("/");


  return (
    <Layout>
      <form className="w-full mx-auto flex flex-col max-w-sm pt-4" onSubmit={handleSubmit}>
        <div className="mb-16 flex flex-col">
            <h1 className="text-4xl text-center text-white font-extrabold">
              Foodbank sign up
            </h1>
        </div>
        <div className="mb-6 flex flex-col">
            <label
              className="block text-accents-7 font-bold mb-3 pr-4"
              htmlFor="name"
            >
              Name of the foodbank
            </label>
            <input
              type="name"
              className="bg-accents-1 appearance-none border-2 border-accents-1 rounded w-full py-2 px-4 text- leading-tight focus:outline-none focus:bg-accents-2 focus:border-accents-4"
              id="name"
              name="name"
              required={true}
              value={name}
              onChange={(e) =>
                setName(e.target.value)
              }
            />
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
              required={true}
              value={email}
              onChange={(e) =>
                setEmail(e.target.value)
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
              required={true}
              value={password}
              onChange={(e) =>
                setPassword(e.target.value)
              }
            />
        </div>
        <div className="mb-6 flex flex-col">
            <label
              className="block text-accents-7 font-bold mb-3 pr-4"
              htmlFor="address1"
            >
              Address line 1 (optional)
            </label>
            <input
              type="address1"
              className="bg-accents-1 appearance-none border-2 border-accents-1 rounded w-full py-2 px-4 text- leading-tight focus:outline-none focus:bg-accents-2 focus:border-accents-4"
              id="address1"
              name="address1"
              required={true}
              value={address1}
              onChange={(e) =>
                setAddress2(e.target.value)
              }
            />
        </div>
        <div className="mb-6 flex flex-col">
            <label
              className="block text-accents-7 font-bold mb-3 pr-4"
              htmlFor="address2"
            >
              Address line 2 (optional)
            </label>
            <input
              type="address2"
              className="bg-accents-1 appearance-none border-2 border-accents-1 rounded w-full py-2 px-4 text- leading-tight focus:outline-none focus:bg-accents-2 focus:border-accents-4"
              id="address2"
              name="address2"
              required={true}
              value={address2}
              onChange={(e) =>
                setAddress2(e.target.value)
              }
            />
        </div>
        <div className="mb-6 flex flex-col">
            <label
              className="block text-accents-7 font-bold mb-3 pr-4"
              htmlFor="phone"
            >
              Phone (optional)
            </label>
            <input
              type="phone"
              className="bg-accents-1 appearance-none border-2 border-accents-1 rounded w-full py-2 px-4 text- leading-tight focus:outline-none focus:bg-accents-2 focus:border-accents-4"
              id="phone"
              name="phone"
              required={true}
              value={phone}
              onChange={(e) =>
                setPhone(e.target.value)
              }
            />
        </div>
        <div className="mb-6 flex flex-col">
            {/* <label
              className="block text-accents-7 font-bold mb-3 pr-4"
              htmlFor="postcode"
            >
              Postcode
            </label> */}
            <label
                className={cn("block font-bold mb-3 pr-4",
                postcodeError ? "text-red" : "text-accents-7")}
                htmlFor="postcode"
              >
                {postcodeError ? postcodeError : "Postcode"}
              </label>
            <input
              type="postcode"
              className="bg-accents-1 appearance-none border-2 border-accents-1 rounded w-full py-2 px-4 text- leading-tight focus:outline-none focus:bg-accents-2 focus:border-accents-4"
              id="postcode"
              name="postcode"
              required={true}
              value={postcode}
              onChange={(e) =>
                setPostcode(e.target.value)
              }
            />
        </div>
        <div className="flex justify-center mt-6">
            <button
              className="shadow bg-accents-0 hover:bg-accents-1 transition-colours duration-200 focus:shadow-outline focus:outline-none text-white font-bold py-2 px-4 rounded-lg"
              type="submit"
              onClick={(e) => handleSubmit(e)}
            >
              Create an account
            </button>
        </div>
        {errorMessage ? (
          <div className="flex justify-center">
            <div className="pt-8">
              <p className="text-center text-red-400">Error: {errorMessage}</p>
            </div>
          </div>
        ) : null}
        <div className="flex justify-center pb-20">
          <div className="pt-8">
            <p className="text-center text-accents-6">
              Do you already have an account?<br />
              <Link href="/login">
                <a className="font-bold">Log in</a>
              </Link>
              .
            </p>
          </div>
        </div>
      </form>
    </Layout>
  )
}

export default Signup;