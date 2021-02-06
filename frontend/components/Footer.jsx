import Link from "next/link";

const Footer = () => {
  // const { isAuthenticated } = useAuth();
  return (
    <nav className="w-full flex items-center justify-between flex-wrap bg-primary p-6">
      <Link href="/">
        <a>
          <div className="flex items-center flex-shrink-0 text-white mr-6">
            <img src="/logo.png" className="h-12 mr-3" />
            <span className="font-bold text-xl tracking-tight">
              Food Bank
            </span>
          </div>
        </a>
      </Link>
      <div className="w-full block flex-grow lg:flex lg:items-center lg:w-auto">
        <div className="text-sm lg:flex-grow">

          <Link href="/privacy">
            <a className="block mt-4 lg:inline-block lg:mt-0 text-teal-200 hover:text-purple-500 transition-colours duration-200 mr-4">
              Privacy
            </a>
          </Link>
          <Link href="/about">
            <a className="block mt-4 lg:inline-block lg:mt-0 text-teal-200 hover:text-purple-500 transition-colours duration-200">
              About
            </a>
          </Link>
        </div>
        <div>
          <a href="https://gutechsoc.com/hackathon" target="_blank" className="inline-block text-sm px-4 py-2 leading-none border rounded text-white border-white font-bold hover:border-transparent hover:text-black hover:bg-secondary transition-colours duration-200 mt-4 lg:mt-0">
            Made as part of UofG Hackathon 2021 ❤️
          </a>
        </div>

      </div>
    </nav>
  );
};

export default Footer;
