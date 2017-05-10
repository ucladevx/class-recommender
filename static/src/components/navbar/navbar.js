import React from 'react';
import {NavLink} from 'react-router-dom';
import Config from 'config';
import {DropdownButton, ButtonGroup, Button, MenuItem, Label} from 'react-bootstrap'
import SearchInput, {createFilter} from 'react-search-input'
import Subjects from 'subjects'


// TODO Need to change the Nav Bar so that it actually looks like
// the pic on the facebook group instead of a bullet point list
const KEYS_TO_FILTERS = ['class.name']
const createButton = (name) => (

  <Button bsStyle="primary" bsSize="large" active>Primary button </Button>
);


class NavigationBar extends React.Component {
  constructor(props) {
    super(props);
    this.state = { searchTerm: "", searchStarted: false };
    this.searchUpdated = this.searchUpdated.bind(this);
  }
 searchUpdated (term) {
    this.setState({searchTerm: term, searchStarted: true})
  }


  render(){
    let k = [];
    console.log(this.state);
    const filteredSubjects = Subjects.filter(createFilter(this.state.searchTerm, KEYS_TO_FILTERS))
    let stuff = ["hi", "bye"];
    for(let [name, url] of Config.nav){
      k.push(<Button className = 'navBarButton' bsSize="large"><NavLink className = 'navBarButtonText' to={url} activeClassName="active">{name}</NavLink></Button>);
    }

    return (
      <div>
        <div className='navBarBackground'>
          <div className='navBarGroup'> {k} </div>
        </div>
      </div>
    )
  }
}

export default NavigationBar;
