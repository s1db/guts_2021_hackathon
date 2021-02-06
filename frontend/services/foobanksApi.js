import { api } from "./Api.js";
import useSWR from 'swr'
import { getEmitHelpers } from "typescript";

// import useAuth from '../contexts/auth.js'

// export const createProject = async (project) => {

//   const API_URL = process.env.NEXT_PUBLIC_API_URL

//   try {
//     const res = await api.post(`${API_URL}/projects`, project)
//     return res.data
//   } catch (error) {
//     console.log(error);
//     return false
//   }
// }

// export const updateProject = async (project) => {

//   const API_URL = process.env.NEXT_PUBLIC_API_URL

//   try {
//     const res = await api.put(`${API_URL}/projects/${project.id}`, project)
//     return res.data
//   } catch (error) {
//     console.log(error.response.data);
//     return false
//   }
// }



// export const deleteProject = async (project) => {

//   const API_URL = process.env.NEXT_PUBLIC_API_URL

//   try {
//     const res = await api.delete(`${API_URL}/projects/${project.id}`)
//     return res.data
//   } catch (error) {
//     console.log(error);
//     return false
//   }
// }
const fetcher = (...args) => fetch(...args).then(res => res.json())

export const getCharityList = () => {

  const API_URL = process.env.NEXT_PUBLIC_API_URL

  const charityListUrl = `${API_URL}/charitylist`;

  console.log("url: ", `${API_URL}/charitylist/`)
  const { data, error } = useSWR(charityListUrl, fetcher)

  console.log('data: ', data)
  return { data, error }
  // Load the projects if the user is defined
  // const {
  //   data,
  //   isValidating,
  //   mutate: mutateCharities
  // // } = useSWR((!user || loading) ? false : `${API_URL}/projects?user=${user.id}&_sort=created_at:DESC`, api.get)
  // } = useSWR(`${API_URL}/charitylist/`, api.get)
  // return { data, isValidating, mutateCharities }

}

export const getPostcodeInfo = async (postcode) => {
  try {

    const response = await api.get(`http://api.postcodes.io/postcodes/${postcode}`)
    return response.data.result

  } catch (e) {
    return e
  }
}

// export const getProducts = () => {

//   const API_URL = process.env.NEXT_PUBLIC_API_URL

//   const { loading, user } = useAuth();

//   // Load the projects if the user is defined
//   const {
//     data: { data: products } = {},
//     isValidating,
//     mutate: mutateProducts
//   } = useSWR((!user || loading) ? false : `${API_URL}/controlled-products/me`, api.get)

//   return { products, isValidating, mutateProducts }

// }


// export const sendMessage = async (values) => {
//   const API_URL = process.env.NEXT_PUBLIC_API_URL

//   try {
//     const res = await api.post(`${API_URL}/projects/message`, values)
//     // const res = await api.post(`http://localhost:1337/projects/message`, values)
//     return res.data
//   } catch (error) {
//     console.log(error.response.data);
//     return false
//   }
// }
