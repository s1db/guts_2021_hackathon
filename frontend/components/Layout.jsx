import Nav from "./Nav";
import Footer from "./Footer";
import cn from "classnames";
import Head from "next/head";

const Layout = ({full = false, children}) => {
  return (
    <div>
      <head>
        <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png"/>
        <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png"/>
        <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png"/>
        <link rel="manifest" href="/site.webmanifest"/>
        <link rel="mask-icon" href="/safari-pinned-tab.svg" color="#5bbad5"/>
        <meta name="msapplication-TileColor" content="#da532c"/>
        <meta name="theme-color" content="#ffffff"/>
      </head>
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