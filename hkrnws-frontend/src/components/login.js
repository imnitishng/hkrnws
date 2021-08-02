import React, { useState } from 'react'
import logo from '../assets/logo.png'

import { useHistory } from 'react-router-dom'
import { registerNewUser, loginUser } from '../services/user'

const Login = () => {

  const history = useHistory()
  const defaultErrors = {
    email: '',
    username: '',
    password: '',
    password2: '',
    login: ''
  }
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [password2, setPassword2] = useState('')
  const [email, setEmail] = useState('')
  const [loginMode, setLoginMode] = useState(false)
  const [errors, setErrors] = useState(defaultErrors)

  const registerFormClass = 'flex flex-col items-center justify-center border-2 h-3/4 bg-white p-7'
  const loginFormClass = 'flex flex-col items-center justify-center border-2 h-2/3 bg-white p-7'

  const resetForm = () => {
    setUsername('')
    setPassword('')
    setPassword2('')
    setEmail('')
    document.getElementById('form').reset()
  }

  const handleRegisterClick = async (e) => {
    e.preventDefault()
    setLoginMode(false)
    setErrors(defaultErrors)

    if(email.length > 0)
      try {
        await registerNewUser(email, username, password, password2)
        setLoginMode(true)
      }
      catch(err) {
        setErrors({
          email: err.response.data.email ? err.response.data.email.join(' ') : '',
          username: err.response.data.username ? err.response.data.username.join(' ') : '',
          password: err.response.data.password ? err.response.data.password.join(' ') : '',
          password2: err.response.data.password2 ? err.response.data.password2.join(' ') : '',
          login: ''
        })
        resetForm()
      }
  }

  const handleLoginClick = async (e) => {
    e.preventDefault()
    resetForm()
    setErrors(defaultErrors)

    if(username.length > 0 || password.length > 0) {
      try {
        const response = await loginUser(username, password)
        const userToken = response.data.token
        window.localStorage.setItem('token', userToken)
        history.push('/posts')
      }
      catch(err) {
        window.localStorage.clear()
        setErrors({
          ...errors,
          login: 'Username or password is incorrect.'
        })
      }
    }
    else {
      setLoginMode(true)
    }
  }

  const visibility = { display: loginMode ? 'none' : '' }
  const formSizeClass = loginMode ? loginFormClass : registerFormClass

  return (
    <div className='flex bg-gray-100 items-center justify-center h-screen'>
      <div className={formSizeClass}>
        <img src={logo} className='h-1/2'/>
        <form className='h-1/2 w-11/12 mt-5' id='form'>
          <div className="mb-2" style={visibility}>
            <label className="block text-grey-darker text-sm mb-2" htmlFor="email">
              E-Mail Address <span className='text-red-600'>{errors.email}</span>
            </label>
            <input
              className="shadow appearance-none border border-red rounded w-full py-2 px-3 text-grey-darker mb-3"
              id="email"
              type="text"
              onChange={(e) => {setEmail(e.target.value)}}
            />
          </div>
          <div className="mb-2">
            <label className="block text-grey-darker text-sm mb-2" htmlFor="username">
              Username <span className='text-red-600'>{errors.username}</span>
            </label>
            <input
              className="shadow appearance-none border rounded w-full py-2 px-3 text-grey-darker"
              id="username"
              type="text"
              onChange={(e) => {setUsername(e.target.value)}}
            />
          </div>
          <div className="mb-2">
            <label className="block text-grey-darker text-sm mb-2" htmlFor="password">
              Password <span className='text-red-600'>{errors.password}</span>
            </label>
            <input
              className="shadow appearance-none border border-red rounded w-full py-2 px-3 text-grey-darker mb-3"
              id="password"
              type="password"
              onChange={(e) => {setPassword(e.target.value)}}
            />
          </div>
          <div className="mb-3" style={visibility}>
            <label className="block text-grey-darker text-sm mb-2" htmlFor="email">
              Confirm Password <span className='text-red-600'>{errors.password2}</span>
            </label>
            <input
              className="shadow appearance-none border border-red rounded w-full py-2 px-3 text-grey-darker mb-3"
              id="password2"
              type="password"
              onChange={(e) => {setPassword2(e.target.value)}}
            />
          </div>
        </form>
        <span className='text-red-600'>{errors.login}</span>
        <div className="flex items-center justify-between w-full">
          <button className="bg-hkrnws-500 hover:bg-hkrnws-600 text-white py-2 px-4 rounded" onClick={handleLoginClick}>
            Sign In
          </button>
          <button className="bg-hkrnws-500 hover:bg-hkrnws-600 text-white py-2 px-4 rounded" onClick={handleRegisterClick}>
            Register
          </button>
        </div>
      </div>
    </div>
  )
}

export default Login
