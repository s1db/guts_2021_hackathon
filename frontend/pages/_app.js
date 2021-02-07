import { AuthProvider } from "../services/auth";
import Head from 'next/head';
import '../assets/main.css';

function App({ Component, pageProps }) {
  return (
    <AuthProvider>
      <Head>
        <title>Foodbank</title>
        <link
          href="https://api.mapbox.com/mapbox-gl-js/v1.10.1/mapbox-gl.css"
          rel="stylesheet"
        />
        <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png"/>
        <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png"/>
        <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png"/>
        <link rel="manifest" href="/site.webmanifest"/>
        <link rel="mask-icon" href="/safari-pinned-tab.svg" color="#5bbad5"/>
        <meta name="msapplication-TileColor" content="#da532c"/>
        <meta name="theme-color" content="#ffffff"/>

        <meta property="og:title" content="Foodbank" />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="https://foobdbank.com/" />
        <meta property="og:image" content="/thumbnail.png" />
        <meta property="og:description" content="Asking for food while in need shouldn't be taboo. Food is a human right. A network of foodbanks to provide support when times are rough." />
        
      </Head>
      <Component {...pageProps} />
    </AuthProvider>
  );
}
export default App;
