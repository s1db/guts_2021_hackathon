import Layout from "../components/Layout";
import Link from "next/link";
import FilterLabel from "../components/FilterLabel";
import { useState } from "react";
import ReactMapboxGl, { Layer, Feature, Marker } from 'react-mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import cn from "classnames";
import { getCharityList, getPostcodeInfo } from '../services/foobanksApi.js'

const Map = ReactMapboxGl({
  accessToken:
    'pk.eyJ1IjoibW91bnRpbnkiLCJhIjoiY2trc3B2a2I3MGRidzJ1bG1pbWFrbzNocyJ9.j3oXww2jPMt109mHKe1Xgg'
});

const foodbanks = [
  {
    name: "Foodbank",
    address: "3 Dalnair Street, Glasgow",
    postcode: "G3 8SD",
    geo: [-4.2858, 55.8698]

  },
  {
    name: "Foodbank",
    address: "3 Dalnair Street, Glasgow",
    postcode: "G3 8SD",
    geo: [-4.2758, 55.8698]

  },
  {
    name: "Foodbank",
    address: "3 Dalnair Street, Glasgow",
    postcode: "G3 8SD",
    geo: [-4.2758, 55.8798]

  },
  {
    name: "Foodbank",
    address: "3 Dalnair Street, Glasgow",
    postcode: "G3 8SD",
    geo: [-4.2858, 55.8798]

  }
]


const diets = {
  vegan: {
    name: "Vegan",
    selected: false
  },
  gluten: {
    name: "Gluten-free",
    selected: false
  },
  sanitary: {
    name: "Sanitary products",
    selected: false
  },
  halal: {
    name: "Halal",
    selected: false
  },
  vegetarian: {
    name: "Vegetarian",
    selected: false
  },
  kosher: {
    name: "Kosher",
    selected: false
  },
  lactose: {
    name: "Lactose-free",
    selected: false
  }
}

const MapPage = () => {
  const [postcode, setPostcode] = useState("")
  const [postcodeError, setPostcodeError] = useState(null)
  const [filters, setFilters] = useState(diets)

  const handleFiltersChange = (name) => {

    const newFilters = {...filters}
    newFilters[name] = {
      ...newFilters[name],
      selected: !newFilters[name].selected
    }
    setFilters(newFilters)
  }

  // const {data, error } = getCharityList()

  // console.log('Charities: ', data)

  const handleMarkerClick = () => {
    console.log('Marker clicked')
  }

  const handleListItemClick = () => {
    console.log('List item click')
  }

  const handleSearchPostcode = async () => {

    setPostcodeError(null);
    if (postcode.length < 3 || postcode.length > 9) {
      setPostcodeError("The postcode is invalid.")
      return
    }
    // api.get(`http://api.postcodes.io/postcodes/${postcode}`).then((res) => {
    //   console.log('REsponse: ', res)
    // })
    try {

      const result = await getPostcodeInfo(postcode)
      console.log('result: ', result)

    } catch (e) {
      setPostcodeError("The postcode is invalid.")
    }
    // // const response = postcodeInfo.json()
    // console.log('postcode info: ', data)
  }
  const handlePostcodeChange = (target) => {
    setPostcodeError(null);
    setPostcode(target)
  }
  
  
  return (
    <Layout full={true}>
      <div className="h-full fit max-fit flex flex-col md:flex-row">
       
        <Map
          style="mapbox://styles/mapbox/streets-v9"
          className="fit"
          center={[-4.2858, 55.8698]}
          containerStyle={{
            height: '100%',
            width: '100%'
          }}
        >
          {
            foodbanks.map((fb, key) => (
              <Marker
                key={key}
                coordinates={fb.geo}
                onClick={handleMarkerClick}
                anchor="bottom" >
                <img src={"marker.svg"}/>
              </Marker>
            ))
          }
         
        </Map>
        <aside className="w-2/5 max-h-full overflow-scroll fit flex flex-col justify-start items-center">

          <div className="w-full py-8 px-4 relative bg-primary-2 rounded-lg">
            <h2 className="text-3xl font-extrabold pb-8">
              Foodbanks close to <span className="text-purple-500">Glasgow</span>
            </h2>
            <div className="mb-6 flex flex-col">
              <label
                className={cn("block font-bold mb-3 pr-4",
                postcodeError ? "text-red" : "text-accents-7")}
                htmlFor="postcode"
              >
                {postcodeError ? postcodeError : "Search for locations"}
              </label>
              <div className="flex">
                
                <input
                  type="text"
                  className="bg-accents-0 mr-4 appearance-none border-2 border-accents-1 rounded w-full py-2 px-4 text- leading-tight focus:outline-none focus:bg-accents-2 focus:border-accents-4"
                  id="postcode"
                  name="postcode"
                  placeholder="Postcode"
                  value={postcode}
                  onChange={(e) =>
                    handlePostcodeChange(e.target.value)
                  }
                />
                <button 
                  className="px-3 py-2 text-sm bg-purple-500 hover:bg-indigo-600 transition-colors duration-200 rounded-lg text-white font-bold"
                  onClick={handleSearchPostcode}
                  >
                  Search
                </button>
              </div>
            </div>
            <div className="flex flex-wrap">
                {
                  Object.keys(filters).map((name, key) => (
                    <FilterLabel 
                      key={key}
                      name={name}
                      text={filters[name].name} 
                      selected={filters[name].selected}
                      handleClick={(name) => handleFiltersChange(name)} />
                  ))
                }
            </div>

          </div>

          <div className="w-full flex flex-col justify-start px-4 py-4">
          {
            foodbanks.map((fb, key) => (
              <div key={key} className="w-full mb-4 p-4 relative bg-accents-0 rounded-lg cursor-pointer" onClick={handleListItemClick}>
                <h3 className="text-2xl pb-4 font-bold text-white">{fb.name} {key}</h3>
                <p className="font-medium text-white pb-8">{fb.address}</p>
                <div className="flex justify-between items-center">
                  <div className="flex">

                    <Link href="/foodbank">
                      <a className="px-3 py-2 mr-4 text-sm bg-accents-1 hover:bg-primary transition-colors duration-200 rounded-lg text-white font-bold">
                        Details
                      </a>
                    </Link>
                    <Link href="/map">
                      <a className="px-3 py-2 text-sm bg-accents-1 hover:bg-primary transition-colors duration-200 rounded-lg text-white font-bold">
                        Locate
                      </a>
                    </Link>
                  </div>
                  <Link href="/map">
                    <a className="px-3 py-2 text-sm bg-purple-500 hover:bg-indigo-600 transition-colors duration-200 rounded-lg text-white font-bold">
                      Order package
                    </a>
                  </Link>
                </div>
              </div>
            ))
          }

          </div>
          
        </aside>
      </div>
    </Layout>
  )
}

export default MapPage;