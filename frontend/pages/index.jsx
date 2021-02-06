import Layout from "../components/Layout";
import React from "react";
import Link from "next/link"
import 'mapbox-gl/dist/mapbox-gl.css';
import { CheckCircledIcon } from '@radix-ui/react-icons'

const HomePage = () => {
  return (
    <Layout>
      <div className="flex flex-col items-center">
        <h1 className="text-6xl mt-12 mb-12 md:text-7xl lg:text-8xl text-center font-bold w-full">
          <span className="py-5 text-transparent bg-clip-text text-center font-bold bg-gradient-to-r from-indigo-400 via-purple-500 to-indigo-600">
            Food is a human right.
          </span>
        </h1>
        <h2 className="text-3xl font-bold text-center">
          A network of foodbanks to provide support when times are rough.
        </h2>
        {/* <div className="w-full flex justify-center items-center">
          <Link href="/map">
            <a href="" className="rounded-lg px-4 py-2 text-2xl text-center font-bold bg-gradient-to-r from-purple-500 to-indigo-600">
              Find nearby foodbank!
            </a>
          </Link>
        </div> */}
        <div className="flex flex-col justify-between items-center mt-20">
          <div className="flex flex-col justify-start items-start bg-accents-0 rounded-2xl px-6 md:px-8 lg:px-12 pt-12 pb-16">

            <h3 className="text-xl md:text-3xl font-extrabold text-purple-500 flex items-center">
              <CheckCircledIcon className="w-8 h-8 mr-4 font-bold" />
              <span>Find the food bank closest to you</span>
            </h3>
            <h3 className="text-xl md:text-3xl font-extrabold text-purple-500 flex items-center pt-8">
              <CheckCircledIcon className="w-8 h-8 mr-4 font-bold" />
              <span>Filter any dietary needs you have</span>
            </h3>
            <h3 className="text-xl md:text-3xl font-extrabold text-purple-500 flex items-center pt-8">
              <CheckCircledIcon className="w-8 h-8 mr-4 font-bold" />
              <span>Discrete food package order</span>
            </h3>

          </div>
          <div className="relative">
            <Link href="/map">
              <a href="" className="rounded-lg ml-0 px-8 py-6 text-lg sm:text-xl lg:text-2xl font-extrabold uppercase text-center font-bold bg-gradient-to-r from-purple-500 to-indigo-600">
                Find nearby foodbank!
              </a>
            </Link>
          </div>
        </div>

      </div>
    </Layout>
  )
}

export default HomePage;