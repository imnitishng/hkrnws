import React from 'react'
import {
  BrowserRouter as Router,
  Switch, Route
} from 'react-router-dom'

import Login from './components/login'
import Posts from './components/posts'

const App = () => {

  return (
    <Router>
      <Switch>
        <Route path="/posts">
          <Posts />
        </Route>
        <Route path="/">
          <Login />
        </Route>
      </Switch>
    </Router>
  )
}


export default App
