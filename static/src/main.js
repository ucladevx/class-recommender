import 'main.scss';

import React from 'react';
import {Provider} from 'react-redux';
import {Route, Switch, Redirect} from 'react-router-dom';
import {ConnectedRouter} from 'react-router-redux';
import {render} from 'react-dom';

import {store, history} from 'reducer';

import Navbar from 'components/navbar/navbar';
import Home from 'components/home';
import Account from 'components/account';
import Scans from 'components/scans';
import ManageScans from 'components/managescans';
import Contact from 'components/contact';
 
// This main.js file will be the center point of at least the Bruin Scanner part of the website. 

// TODO We need to include the bruin scan logo above the navbar
// TODO Navbar needs to be improved. That code can be found in view/navbar.js
// TODO We need to figure out the content in the Account tab. Code in container/account.js
// TODO We need to figure out the content in the Scans tab. Code in container/scans.js
// TODO We need to figure out the content in the Manage Scans tab. Code in container/managescans.js
// TODO We need to figure out the content in the Contact tab. Code in container/contact.js
// TODO We need to make the HTML dropdown menu look nicer and the different sessions
// should cause different changes in the classes that we list. 
// TODO Need to figure out who is currently logged in, and need to put their name in the top left corner
// TODO Need to figure out what to do when the user clicks the logout button
// TODO Create two React Dropdown menus (one for majors and one for classes). These should be dynamic
// because we are getting them from some database with that information. 
// TODO Display the class name and pre requisites right underneath the two dropdowns
// TODO Show sections and class timings and graph of grades


class App extends React.Component {
  render(){
    return <div><Provider store={store}>
      <ConnectedRouter history={history}>
        <div>
          <Navbar/>
          <Switch>
            <Route exact path="/" component={Home}/>
            <Route path="/account" component={Account}/>
            <Route path="/scans" component={Scans}/>
            <Route path="/managescans" component={ManageScans}/>
            <Route path="/contact" component={Contact}/>
            <Redirect to="/"/>
          </Switch>
        </div>
      </ConnectedRouter>
    </Provider>
    <div className='bottomBlueBar'></div>
 </div>
  }
}


render(
  <App/>,
  document.getElementById('mount')
);
