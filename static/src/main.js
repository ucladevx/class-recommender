import 'main.scss';

import React from 'react';
import {Provider} from 'react-redux';
import {Route, Switch, Redirect} from 'react-router-dom';
import {ConnectedRouter} from 'react-router-redux';
import {render} from 'react-dom';

import {store, history} from 'reducer';

import Navbar from 'view/navbar';
import Home from 'container/home';
import Account from 'container/account';
import Scans from 'container/scans';
import ManageScans from 'container/managescans';
import Contact from 'container/contact';
 
// TODO We need to include the bruin scan logo above the navbar
// TODO Navbar needs to be improved. That code can be found in view/navbar.js
// TODO We need to figure out the content in the Account tab. Code in container/account.js
// TODO We need to figure out the content in the Scans tab. Code in container/scans.js
// TODO We need to figure out the content in the Manage Scans tab. Code in container/managescans.js
// TODO We need to figure out the content in the Contact tab. Code in container/contact.js
// TODO We need to make the HTML dropdown menu look nicer and the different sessions
// should cause different changes in the classes that we list. 
//


class App extends React.Component {
  render(){
    return <Provider store={store}>
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
          <select>
            <option>Summer Session A - 2017</option>
            <option>Summer Session B - 2017</option>
            <option>Summer Session C - 2017</option>
          </select>
        </div>
      </ConnectedRouter>
    </Provider>;
  }
}


render(
  <App/>,
  document.getElementById('mount')
);
