import Layout from "../components/Layout";
import ReactMapboxGl, { Layer, Feature, Marker } from 'react-mapbox-gl';
import { useEffect, useState } from "react";
import { useRouter } from "next/router";


const Map = ReactMapboxGl({
  accessToken:
    'pk.eyJ1IjoibW91bnRpbnkiLCJhIjoiY2trc3B2a2I3MGRidzJ1bG1pbWFrbzNocyJ9.j3oXww2jPMt109mHKe1Xgg'
});


const Me = () => {

  const router = useRouter()
  const [u, setU] = useState({
    name: "Welcome Glasgow Southeast Foodbank",
    email: "mikllhor@gmail.com",
    latitude: 55.840181,
    longitude: -4.256667,
    phone: "0751 782 9084"
  })


  useEffect(() => {

    const auth = window.localStorage.getItem("auth");
    const user = window.localStorage.getItem("user");
    if (user) {
      const parsedUser = JSON.parse(user)
      setU(parsedUser)

    }

    if (auth === "false") {
      router.push("/login")
    }

  },[])

  
  return (
    <Layout>
      <h1 className="text-3xl font-bold pt-3 pb-5">Welcome, {u.name}!</h1>
      <span className="font-medium text-xl">Profile details</span>
      <ul className="mt-4">
        <li>Email: {u.email}</li>
        <li>Phone: {u.phone}</li>
      </ul>
      <Map
          style="mapbox://styles/mapbox/streets-v9"
          className="w-full mt-16"
          center={[u.longitude, u.latitude]}
          containerStyle={{
            height: '40vh',
            width: '100%'
          }}
        >
          {
              <Marker
                coordinates={[u.longitude, u.latitude]}
                anchor="bottom" >
                <img src={"marker.svg"}/>
              </Marker>
          }
         
        </Map>
    </Layout>
  );

}

export default Me;