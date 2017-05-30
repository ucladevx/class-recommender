// TODO figure out why home.scss can't be resolved. I get an error whenever I try to load it in. 

//import 'home.scss';
import React from 'react';
import {connect} from 'react-redux';

import Config from 'config';
import Dropdown from 'react-dropdown'
import {DropdownButton, ButtonGroup, Button, MenuItem} from 'react-bootstrap'
import SearchInput, {createFilter} from 'react-search-input'
import Subjects from 'subjects'

// This home.js file will serve as the home page for the class scanner portion of the project

class ClassDropdown extends React.Component {
  constructor(props) {
    super(props);
    this.state = { searchTerm: "", searchStarted: false, classList: [] };
    this.searchUpdated = this.searchUpdated.bind(this);
  }
  searchUpdated (term) {
    this.setState({searchTerm: term, searchStarted: true})
  }

  onItemClick(item, e) {  
    console.log(item.subject);
  }

  render(){

    if(!this.props.classList)
      this.props.classList = [];

    let KEYS_TO_FILTERS = [];

    if(!this.props.classList)
       KEYS_TO_FILTERS = [];
    else{
      KEYS_TO_FILTERS = ['name'];
    }

    var list = this.props.classList;

    console.log("Keys to filters");
    console.log(this.props.classList);
    const filteredSubjects = this.props.classList.filter(createFilter(this.state.searchTerm, KEYS_TO_FILTERS))
    return(
    <div>
      <div className = "ClassDropdownContainer">
        <SearchInput className='search-input' onChange={this.searchUpdated} />
            <div className = 'ClassDropdown'>
              {filteredSubjects.map(list => {
                  let itemClick = this.onItemClick.bind(this, this.props.classList);
                  return (
                    <div className = "dropdownItem" key={this.props.classList.tag} onClick={itemClick}>
                      {this.props.classList.name}
                    </div>
                  )
              })}
            </div>
      </div>
    </div>
    )
  }
}

function test() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
             console.log(this.responseText);
        }
    };
    xhttp.open("GET", "http://localhost:5000", true);
    xhttp.send();
}


const mapStateToProps = (state)=>{
  return {
    urlPath: state.router.location.pathname,
  };
};

const mapDispatchToProps = (dispatch)=>{
  return {
    printlog: (input)=>{
      console.log(input);
      // dispatch(action);
    },
  };
};

export default ClassDropdown;
