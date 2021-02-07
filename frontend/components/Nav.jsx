import Link from "next/link";
import { useAuth } from "../services/auth";
import { useRouter } from "next/router";
import { useEffect, useState } from "react";

const Nav = () => {
  
  const [isAuthenticated, setAuthenticated] = useState(false)
  
  
  useEffect(() => {
    const auth = window.localStorage.getItem("auth");
    if (auth === "true") {
      setAuthenticated(true)
    }

  }, [])

  const router = useRouter()



  const handleLogout = (e) => {
    e.preventDefault();

    window.localStorage.setItem("auth", false)
    router.push("/")
  }

  return (
    <nav className="flex items-center justify-between bg-teal-500 p-6">
      <Link href="/">
        <a>
          <div className="flex items-center text-white pr-6">
            <img src="/logo.png" className="h-12 mr-3" />
            <span className="font-bold text-2xl tracking-tight">
              Food&nbsp;Bank
            </span>
            <h4 className="text-sm hidden md:block pl-6">
              Easier&nbsp;access&nbsp;to&nbsp;food&nbsp;for&nbsp;everyone.
            </h4>
          </div>
        </a>
      </Link>
      <div className="w-full block flex items-center justify-end">
        <div className="text-sm flex-grow">
       
        </div>
          
          {isAuthenticated ? (
            <Link href="/me">
              <a className="block mr-8 inline-block mt-0 text-teal-200 hover:text-white">
                Profile
              </a>
            </Link>
          ) : (<Link href="/about">
          <a className="block mr-8 inline-block mt-0 text-teal-200 hover:text-white">
            About
          </a>
        </Link>)}
          {isAuthenticated ? (

              <button onClick={(e) => handleLogout(e)} className="inline-block text-sm px-4 py-2 leading-none border rounded text-white border-white font-bold hover:border-transparent hover:text-black hover:bg-secondary transition-colours duration-200">
                Logout
              </button>

          ) : 
            router.pathname !== "/login" && router.pathname !== "/signup" && (

              <Link href="/login">
                <a className="inline-block text-sm px-4 py-2 leading-none border rounded text-white border-white font-bold hover:border-transparent hover:bg-secondary hover:text-black transition-colours duration-200">
                  Login
                </a>
              </Link>
            ) 
          }
      </div>
    </nav>
  );
};

export default Nav;
