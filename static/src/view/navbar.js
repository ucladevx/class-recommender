import React from 'react';
import {NavLink} from 'react-router-dom';
import Config from 'config';

// TODO Need to change the Nav Bar so that it actually looks like 
// the pic on the facebook group instead of a bullet point list

class Navbar extends React.Component {
  render(){
    let k = [];
    for(let [name, url] of Config.nav){
      k.push(<li><NavLink to={url} activeClassName="active">{name}</NavLink></li>);
    }
    return (<div>
      <ul>
        {k}
      </ul>
    </div>)
  }
}

export default Navbar
