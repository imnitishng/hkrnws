import React, { useState } from 'react'

import { updatePostStatus } from '../services/posts'

const Post = ({ post }) => {
  const [visibility, setVisibility] = useState(true)
  const [read, setRead] = useState(false)

  const handleHidePostClick = (e) => {
    e.preventDefault()
    updatePostStatus(post.id, 'hide').then(
      () => {
        setVisibility(false)
      }
    )
  }

  const handleMarkPostAsRead = (e) => {
    e.preventDefault()
    updatePostStatus(post.id, 'read').then(
      () => {
        console.log(`read ${post.id}`)
        setRead(true)
        window.open(e.target.href, '_blank')
      }
    )
  }

  // Handle discussion posts, no comment number is present for these posts on HN
  // they only have a single `discuss` button in place of comments
  let comments
  if(post.comments === 'discuss')
    comments = 'discuss'
  else
    comments = `${post.comments} comments`

  let visible
  visible = { display: visibility ? '' : 'none' }
  visible = { display: post.deleted ? 'none' : '' }

  let postCSSClass
  postCSSClass = (post.read || read) ?
    { postClass: 'my-1 border-1 bg-gray-200', textColor: 'text-gray-400', pointColor: 'font-bold md:text-xl text-hkrnws-300' } :
    { postClass: 'my-1 border-1 bg-white',  textColor: 'text-black', pointColor: 'font-bold md:text-xl text-hkrnws-400' }

  return (
    <li className={postCSSClass.postClass} style={visible}>
      <div className='flex flex-row items-center justify-start'>
        <div className='w-12 md:w-16 pl-1'>
          <span className={postCSSClass.pointColor}>
            {post.points}
          </span>
        </div>
        <div className='flex flex-row justify-between w-full'>
          <div className='flex flex-col mt-1'>
            <span className={postCSSClass.textColor}>
              <button onClick={handleMarkPostAsRead}>
                <a href={post.hn_post_url}>{post.title}</a>
              </button>
            </span>
            <span className='text-xxs text-hkrnws-700 w-40 truncate' >
              <button onClick={handleMarkPostAsRead}>
                <a href={post.story_url}>{post.story_url}</a>
              </button>
            </span>
            <div className='text-xs text-gray-400 mb-1'>
              <a href={post.poster_profile_url}>{post.posted_by}</a> |&nbsp;
              <button onClick={handleMarkPostAsRead}>
                <a href={post.hn_post_url}>{comments}</a>
              </button> |&nbsp;
              {post.post_age.split('.')[0]} hrs ago
            </div>
          </div>
          <div className='flex items-center pr-2'>
            <button onClick={handleHidePostClick}>
              <img src="https://img.icons8.com/material-sharp/24/000000/hide.png"/>
            </button>
          </div>
        </div>
      </div>

    </li>
  )
}

export default Post
