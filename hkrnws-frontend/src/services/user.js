import axios from 'axios'

const hostURL = 'http://localhost:8000'
const baseURL = `${hostURL}/api`

export const registerNewUser = async (email, username, password, password2) => {
  const requestBody = {
    email: email,
    username: username,
    password: password,
    password2: password2
  }

  const response = await axios.post(`${baseURL}/users/register/`, requestBody)
  return response
}

export const loginUser = async (username, password) => {
  const requestBody = {
    username: username,
    password: password
  }

  const response = await axios.post(`${baseURL}/api-token-auth/`, requestBody)
  return response
}
