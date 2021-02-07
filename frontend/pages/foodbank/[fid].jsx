import { useRouter } from 'next/router'
import Layout from "../../components/Layout";
import React from "react";
import Link from "next/link"
import 'mapbox-gl/dist/mapbox-gl.css';
import { CheckCircledIcon } from '@radix-ui/react-icons'
import ReactMapboxGl, { Layer, Feature, Marker } from 'react-mapbox-gl';

const Map = ReactMapboxGl({
  accessToken:
    'pk.eyJ1IjoibW91bnRpbnkiLCJhIjoiY2trc3B2a2I3MGRidzJ1bG1pbWFrbzNocyJ9.j3oXww2jPMt109mHKe1Xgg'
});


const FoodbankPage = ({ charity }) => {
  const router = useRouter()

  console.log(charity)

  return (
    <Layout>
      <div className="flex flex-col items-center pb-20">
        <h1 className="text-6xl mt-12 mb-12 md:text-7xl lg:text-8xl text-center font-bold w-full">
          <span className="py-5 text-transparent bg-clip-text text-center font-bold bg-gradient-to-r from-indigo-400 via-purple-500 to-indigo-600">
            {charity.name}
          </span>
        </h1>
        <h2 className="text-3xl font-bold text-center">
          We are here for you ✌️
        </h2>

        <div className="w-full">
          <h2 className="text-2xl font-bold text-left mt-16">
            Phone: {charity.phone}
          </h2>
          <h2 className="text-2xl font-bold text-left mt-8">
            Address: {charity.address}
          </h2>
        </div>

        <Map
          style="mapbox://styles/mapbox/streets-v9"
          className="w-full mt-16"
          center={[charity.geo[0], charity.geo[1]]}
          containerStyle={{
            height: '40vh',
            width: '100%'
          }}
        >
          {
              <Marker
                coordinates={[charity.geo[0], charity.geo[1]]}
                anchor="bottom" >
                <img src={"/marker.svg"}/>
              </Marker>
          }
         
        </Map>

      </div>
    </Layout>
  )
}

export default FoodbankPage


export async function getServerSideProps({context, query}) {
    
  const foodbanks = [
    {
      pk: 1,
      name: "Glasgow NW Foodbank",
      address: "33 Kinstone Avenue, Scotstoun, Glasgow",
      postcode: "G14 0EB",
      geo: [-4.363900, 55.885257],
      phone: "0766 787 9088"
    },
    {
      pk: 2,
      name: "Glasgow SE Foodbank",
      address: "42 Inglefield Street, Glasgow",
      postcode: "G42 7AT",
      geo: [-4.256667, 55.840181],
      phone: "0766 787 9088"
    },
    {
      pk: 3,
      name: "Glasgow NE Foodbank",
      address: "3 Dalnair Street, Glasgow",
      postcode: "G31 4NA",
      geo: [-4.198709, 55.848159],
      phone: "0766 787 9088"
    },
    {
      pk: 5,
      name: "Drumchapel Foodbank",
      address: "Ladyloan Place Unit 9, Glasgow",
      postcode: "G15 8LB",
      geo: [-4.379215, 55.917106],
      phone: "0766 787 9088"
    }
  ]

  const charity = foodbanks.find(element => element.pk === parseInt(query.fid));

  return {
    props: {
      charity
    }, // will be passed to the page component as props
  }
}