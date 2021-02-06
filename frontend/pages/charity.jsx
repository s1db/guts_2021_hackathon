import Layout from "../components/Layout";
import { CheckCircledIcon } from '@radix-ui/react-icons'
import ReactMapboxGl, { Layer, Feature, Marker } from 'react-mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';

const MapPage = () => {
    return (    
    <Layout>
        <div className="flex">

            <div className=" flex-1">
                <div className="h-full bg-gradient-to-r from-indigo-400 via-purple-500 to-indigo-600">
                    hey
                </div>
            </div>

            <div className=" flex-1 px-10">

                <h1 className="text-3xl mt-12 mb-12 md:text-4xl lg:text-5xl font-bold w-full">
                    <span className="py-5 text-transparent bg-clip-text font-bold bg-gradient-to-r from-indigo-400 via-purple-500 to-indigo-600">
                        charity.charityname
                    </span>
                </h1>
                
                <div className="py-3">                
                    <h3 className="text-gray-400">
                        <p> You can find us at: </p>  
                    </h3>
                    <h2 className="font-bold ">
                        <p> charity.city, charity.address </p> 
                    </h2>
                </div>
                
                <div className="py-3">                
                    <h3 className="text-gray-400">
                        <p> Email: </p>  
                    </h3>
                    <h2 className="font-bold ">
                        <p> charity.email </p> 
                    </h2>
                </div>

                <div className="py-3">                
                    <h3 className="text-gray-400">
                        <p> Phone: </p>  
                    </h3>
                    <h2>
                        <p> charity.phone </p> 
                    </h2>
                </div>
                <div className="py-4">
                    <a class="px-3 py-2 text-sm bg-purple-500 hover:bg-indigo-600 transition-colors duration-200 rounded-lg text-white font-bold" href="/map">Order package</a>
                </div>
                
            </div>
        </div>
    </Layout>
    )
}

export default MapPage;