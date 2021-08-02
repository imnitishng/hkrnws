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

  const registerFormClass = 'w-1/2 border-2 h-max bg-white p-7 relative'
  const loginFormClass = 'w-1/2 border-2 h-max bg-white p-7 relative'

  const resetForm = () => {
    setUsername('')
    setPassword('')
    setPassword2('')
    setEmail('')
    document.getElementById('form').reset()
  }

  const handleRegisterClick = async (e) => {
    e.preventDefault()

    try {
      await registerNewUser(email, username, password, password2)
      handleFormLoginMode(true)
    }
    catch(err) {
      setErrors({
        email: err.response.data.email ? err.response.data.email.join(' ') : '',
        username: err.response.data.username ? err.response.data.username.join(' ') : '',
        password: err.response.data.password ? err.response.data.password.join(' ') : '',
        password2: err.response.data.password2 ? err.response.data.password2.join(' ') : '',
        login: ''
      })
    }
  }

  const handleLoginClick = async (e) => {
    e.preventDefault()
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

  const handleFormLoginMode = (arg) => {
    resetForm()
    setErrors(defaultErrors)
    setLoginMode(arg)
  }

  const visibility = { display: loginMode ? 'none' : '' }
  const loginButton = { display: loginMode ? '' : 'none' }
  const registerButton = { display: loginMode ? 'none' : '' }
  const formSizeClass = loginMode ? loginFormClass : registerFormClass

  return (
    <div className='flex bg-gray-100 items-center justify-center h-screen'>
      <div className={formSizeClass}>
        <div className='flex flex-row justify-center'>
          <div className='flex flex-col items-center w-full'>
            <img src={logo} className='w-full'/>

            <form className='h-1/2 w-full mt-5 my-auto' id='form'>
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

            <button className="bg-white hover:bg-hkrnws-200 text-hkrnws-700 px-4 mb-10 w-full" style={loginButton} onClick={handleLoginClick}>
              Sign In
            </button>
            <button className="bg-white hover:bg-hkrnws-200 text-hkrnws-700 px-4 mb-10 w-full" style={registerButton} onClick={handleRegisterClick}>
              Register
            </button>

            <div className="flex flex-col justify-between w-full absolute bottom-0">
              <div className='bg-hkrnws-500 h-3 w-full'></div>
              <div className='flex flex-row items-center'>
                <button className="bg-white hover:bg-hkrnws-200 text-hkrnws-700 py-2 px-4 w-full" onClick={() => handleFormLoginMode(true)}>
                  Existing User
                </button>
                <button className="bg-white hover:bg-hkrnws-200 text-hkrnws-700 py-2 px-4 w-full" onClick={() => handleFormLoginMode(false)}>
                  New User
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Login
