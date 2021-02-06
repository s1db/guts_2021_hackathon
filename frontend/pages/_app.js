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
      </Head>
      <Component {...pageProps} />
    </AuthProvider>
  );
}
export default App;
