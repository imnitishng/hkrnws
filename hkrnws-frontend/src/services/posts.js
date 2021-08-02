import axios from 'axios'

const hostURL = 'http://localhost:8000'
const baseURL = `${hostURL}/api`

export const fetchPosts = async () => {
  const headers = {
    'Authorization': `Token ${window.localStorage.getItem('token')}`,
  }
  const requestBody = {
    method: 'get',
    url: `${baseURL}/posts/`,
    headers: headers,
  }

  const response = await axios(requestBody)
  return response
}

export const updatePostStatus = async (postID, action) => {
  const headers = {
    'Authorization': `Token ${window.localStorage.getItem('token')}`,
  }
  const data = {
    id: postID,
    action: action
  }
  const requestBody = {
    method: 'post',
    url: `${baseURL}/post/`,
    headers: headers,
    data: data
  }

  const response = await axios(`${baseURL}/post/`, requestBody)
  return response
}
