import Layout from "../components/Layout";

const About = () => {
  return (    
  <Layout>
    <div className="divide-y divide-purple-500">

      <div className="pb-20"> 
        <h1 className="text-4xl mt-12 mb-24 md:text-5xl lg:text-6xl text-center font-bold w-full">
          <span className="py-6 text-white text-center font-bold ">
            Asking for food while in need shouldn't be taboo.
          </span>
        </h1>

        <div className="container py-6 flex max-h-full w-full">

          <div className="flex-1 self-center"> 
            <div className="px-20">
              <h2 className="py-3 text-3xl text-gray-300 text-center">
                On this site you can look where to ask for food when you are in need. 
              </h2> 

              <h2 className="py-3 text-3xl text-gray-200 text-center font-bold">
                Without judgement. 
              </h2>
            </div>
          </div>

          <div className="flex-1 w-full"> 
            <img src="/foodbank.jpg" alt="Food Bank" className="rounded-full" />
          </div>

        </div>
      </div>
      
      <div>
        <div className="py-6" >
          <h2 className="py-3 text-3xl text-gray-300 text-center">
            This is a project developed during the hackathon 'Do you have the GUTS 2021'.
          </h2>         
          <h2 className="py-3 text-3xl text-gray-500 text-center">
            The team:
          </h2> 
        </div>

        <div className="flex py-10r">

      <div className="flex-1 w-full p-10"> 
        <img src="/contributors/shrek.jpg" alt="Food Bank" className="rounded-full block " />
        <p className="py-3 block text-center w-full font-bold">
          Blackadder
        </p>
        <p className="block text-center w-full">
          frontend
        </p>
      </div>        
      
      <div className="flex-1 w-full p-10"> 
        <img src="/contributors/shrek.jpg" alt="Food Bank" className="rounded-full block" />
        <p className="py-3 block text-center w-full font-bold">
          Cromos
        </p>
        <p className="block text-center w-full">
          "frontend"
        </p>
      </div>   

      <div className="flex-1 w-full p-10"> 
        <img src="/contributors/shrek.jpg" alt="Food Bank" className="rounded-full block" />
        <p className="py-3 block text-center w-full font-bold">
          MongoDB
        </p>
        <p className="block text-center w-full">
          backend
        </p>
      </div>  

      <div className="flex-1 w-full p-10"> 
        <img src="/contributors/shrek.jpg" alt="Food Bank" className="rounded-full block" />
        <p className="py-3 block text-center w-full font-bold">
          Sid
        </p>
        <p className="block text-center w-full">
          backend
        </p>
      </div>  

      <div className="flex-1 w-full p-10"> 
        <img src="/contributors/shrek.jpg" alt="Food Bank" className="rounded-full block" />
        <p className="py-3 block text-center w-full font-bold">
          Vinlenka
        </p>
        <p className="block text-center w-full">
          backend
        </p>
      </div>   

    </div>
      </div>
    </div>
  </Layout>
  )
}

export default About;