import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export async function generateListing(formData, files) {
  const multipart = new FormData()
  multipart.append('payload', JSON.stringify(formData))
  files.forEach((file) => multipart.append('images', file))

  const { data } = await axios.post(`${API_BASE_URL}/api/listings/generate`, multipart, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })

  return data
}
