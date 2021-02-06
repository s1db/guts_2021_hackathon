import Link from "next/link";
import { useAuth } from "../lib/auth";
import { useRouter } from "next/router";

const Nav = () => {
  const { isAuthenticated } = useAuth();

  const router = useRouter()

  return (
    <nav className="flex items-center justify-between bg-teal-500 p-6">
      <Link href="/">
        <a>
          <div className="flex items-center flex-shrink-0 text-white mr-6">
            <img src="logo.png" className="h-12 mr-3" />
            <span className="font-bold text-2xl tracking-tight">
              Food Bank
            </span>
          </div>
        </a>
      </Link>
      <div className="w-full block flex-grow lg:flex lg:items-center lg:w-auto">
        <div className="text-sm lg:flex-grow">
          {isAuthenticated ? (
            <Link href="/me">
              <a className="block mt-4 lg:inline-block lg:mt-0 text-teal-200 hover:text-white mr-4">
                Profile
              </a>
            </Link>
          ) : null}
          {/* <Link href="/ping">
            <a className="block mt-4 lg:inline-block lg:mt-0 text-teal-200 hover:text-white mr-4">
              Ping
            </a>
          </Link> */}
          <h4 className="text-sm">
            Easier access to food for everyone.
          </h4>
        </div>
        <div>
          <Link href="/about">
            <a className="block mt-4 mr-8 lg:inline-block lg:mt-0 text-teal-200 hover:text-white">
              About
            </a>
          </Link>
          {isAuthenticated ? (
            <Link href="/logout">
              <a className="inline-block text-sm px-4 py-2 leading-none border rounded text-white border-white font-bold hover:border-transparent hover:text-black hover:bg-secondary transition-colours duration-200 mt-4 lg:mt-0">
                Logout
              </a>
            </Link>
          ) : 
            router.pathname !== "/login" && router.pathname !== "/signup" && (

              <Link href="/login">
                <a className="inline-block text-sm px-4 py-2 leading-none border rounded text-white border-white font-bold hover:border-transparent hover:text-black hover:bg-secondary transition-colours duration-200 mt-4 lg:mt-0">
                  Login
                </a>
              </Link>
            ) 
          }
        </div>
      </div>
    </nav>
  );
};

export default Nav;
