import React from 'react';
import {NavLink} from 'react-router-dom';
import Config from 'config';
import {DropdownButton, ButtonGroup, Button, MenuItem, Label} from 'react-bootstrap'

// TODO Need to change the Nav Bar so that it actually looks like 
// the pic on the facebook group instead of a bullet point list

const createButton = (name) => (

  <Button bsStyle="primary" bsSize="large" active>Primary button </Button>
);

class Navbar extends React.Component {
  render(){
    let k = [];
    for(let [name, url] of Config.nav){
      k.push(<Button bsSize="large"><NavLink to={url} activeClassName="active">{name}</NavLink></Button>);
    }


    return (<div>
        {k}
      <Button bsStyle="primary" bsSize="small" active>Primary button </Button>
      <Label bsClass="col-sm-3 text-center">{"hello world"}</Label>
    </div>)
  }
}

export default Navbar
