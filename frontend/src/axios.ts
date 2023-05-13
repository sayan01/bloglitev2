import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'https://bloglite.sayn.work',
  headers: {
    'Content-Type': 'application/json'
  }
})

function setAuthToken(token: string | null) {
  if (token) {
    apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`
  } else {
    delete apiClient.defaults.headers.common['Authorization']
  }
}

export { apiClient, setAuthToken }
