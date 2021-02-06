import { useRouter } from 'next/router'
import Layout from "../../components/Layout";
import React from "react";
import Link from "next/link"
import 'mapbox-gl/dist/mapbox-gl.css';
import { CheckCircledIcon } from '@radix-ui/react-icons'


const FoodbankPage = ({ charity }) => {
  const router = useRouter()

  console.log(charity)

  const { fid } = router.query

  return (
    <Layout>
      <div className="flex flex-col items-center pb-20">
        <h1 className="text-6xl mt-12 mb-12 md:text-7xl lg:text-8xl text-center font-bold w-full">
          <span className="py-5 text-transparent bg-clip-text text-center font-bold bg-gradient-to-r from-indigo-400 via-purple-500 to-indigo-600">
            {charity.charity.charityname}
          </span>
        </h1>
        <h2 className="text-3xl font-bold text-center">
          A network of foodbanks to provide support when times are rough.
        </h2>

      </div>
    </Layout>
  )
}

export default FoodbankPage


export async function getServerSideProps({context, query}) {
  console.log('context: ', query)

  const API_URL = process.env.NEXT_PUBLIC_API_URL

  const charityListUrl = `${API_URL}/charitylist`;

  const res = await fetch(charityListUrl, {
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
  }
  })

  const charities = await res.json()

  let formatted = []

  Object.keys(charities).map((email) => {
    let charity = {
      pk: JSON.parse(charities[email].address)[0].pk,
      email,
      address: JSON.parse(charities[email].address)[0].fields,
      charity: JSON.parse(charities[email].charity)[0].fields,
      diet_options: JSON.parse(charities[email].diet_options)[0].fields
    }
    formatted.push(charity)
  })

  const charity = formatted.find(element => element.pk === parseInt(query.fid));

  return {
    props: {
      charity
    }, // will be passed to the page component as props
  }
}