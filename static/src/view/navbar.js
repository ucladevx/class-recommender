import React from 'react';
import {NavLink} from 'react-router-dom';
import Config from 'config';
import {DropdownButton, ButtonGroup, Button, MenuItem, Label} from 'react-bootstrap'
import SearchInput, {createFilter} from 'react-search-input'
import emails from './mails'

// TODO Need to change the Nav Bar so that it actually looks like
// the pic on the facebook group instead of a bullet point list
const KEYS_TO_FILTERS = ['user.name']
const createButton = (name) => (

  <Button bsStyle="primary" bsSize="large" active>Primary button </Button>
);


class Navbar extends React.Component {
  constructor(props) {
    super(props);
    this.state = { searchTerm: "" };
    this.searchUpdated = this.searchUpdated.bind(this);
  }
 searchUpdated (term) {
    this.setState({searchTerm: term})
  }


  render(){
    let k = [];
    console.log(this.state);
    const filteredEmails = emails.filter(createFilter(this.state.searchTerm, KEYS_TO_FILTERS))
    let stuff = ["hi", "bye"];
    for(let [name, url] of Config.nav){
      k.push(<Button bsSize="large"><NavLink to={url} activeClassName="active">{name}</NavLink></Button>);
    }


    return (<div>
      {createButton("hi")}
        {k}
      <Button bsStyle="primary" bsSize="small" active>Primary button </Button>
      <Label bsClass="col-sm-3 text-center">{"hello world"}</Label>
        <div>
          <SearchInput className='search-input' onChange={this.searchUpdated} />
          {filteredEmails.map(email => {
            return (
              <div className='mail' key={email.id}>
                <div className='from'>{email.user.name}</div>
                <div className='subject'>{email.subject}</div>
              </div>
            )
          })}
        </div>
    </div>
  )
  }
}

export default Navbar
