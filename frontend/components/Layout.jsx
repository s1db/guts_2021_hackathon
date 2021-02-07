import Nav from "./Nav";
import Footer from "./Footer";
import cn from "classnames";
import Head from "next/head";

const Layout = ({full = false, children}) => {
  return (
    <div>
      <Nav />
      <div className={cn("fit mx-auto", !full && "px-6 max-w-7xl")}>
        {children}
      </div>
      {
        !full && (
          <Footer />
        )
      }
      
    </div>
  )
}

export default Layout;