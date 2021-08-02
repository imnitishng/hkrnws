import React, { useState, useEffect } from 'react'
import { useHistory } from 'react-router-dom'

import { fetchPosts } from '../services/posts'
import Post from './post'

const Posts = () => {
  const history = useHistory()
  const [posts, setPosts] = useState([])

  const handleLogout = (e) => {
    e.preventDefault()
    window.localStorage.clear()
    history.push('/')
  }

  useEffect(() => {
    fetchPosts().then(
      response => {
        setPosts(response.data)
      }
    )
  }, [])

  return (
    <div>
      <div className='w-full h-12 bg-hkrnws-400 text-hkrnws-900 text-2xl sticky top-0 flex items-center justify-between px-5'>
        hckrnws
        <button className='text-sm' onClick={handleLogout}>
          Logout
        </button>
      </div>
      <div className="flex justify-center bg-gray-300">
        <ul className="w-11/12 md:w-8/12">
          {posts.map(post =>
            <Post
              key={post.id}
              post={post}
            />)}
        </ul>
      </div>
    </div>
  )
}

export default Posts